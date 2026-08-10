"""`ClienteAnthropic` — a única porta de saída para a API da Anthropic neste
repositório [CLAUDE.md: "nenhuma chamada à API foi feita ainda"; este módulo
é o primeiro a importar `anthropic`].

Escopo estritamente de infraestrutura: aplica como código as regras de custo
e robustez do CLAUDE.md §10 e desta sessão. Não decide o que perguntar, não
monta prompt de conteúdo, não implementa etapa de pipeline — isso é das
funções, que ainda não existem [CLAUDE.md §4, §14].

Cada chamada via `chamar()` é uma "chamada de diagnóstico isolada": recebe um
prefixo estável (`system_estavel`) e as unidades daquela chamada
(`unidades`), sem acumular histórico de mensagens anteriores. É o que garante
tamanho constante entre chamadas e o que os cálculos de `docs/custos.md`
pressupõem — acumular histórico aqui invalidaria a régua de custo inteira.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import anthropic

from .cache_local import CacheLocal, RespostaCache
from .configuracao import ConfiguracaoDeRobustez
from .custo import CustoCalculado, calcular_custo
from .erros import (
    ErroCacheNaoAproveitado,
    ErroEffortAusente,
    ErroMaxTokensAusente,
    ErroRespostaTruncada,
)
from .estado_prefixo import EstadoPrefixo
from .estado_prefixo import carregar as carregar_estado_prefixo
from .estado_prefixo import salvar as salvar_estado_prefixo
from .hash_entrada import hash_prefixo_estavel, hash_requisicao
from .ledger import Ledger, RegistroDeCusto
from .mapeamento import mapear_erro_sdk

# Acima deste limiar de max_tokens, requisição não-streaming corre risco de
# timeout HTTP do lado do SDK [skill claude-api, python/claude-api/streaming.md:
# "Large max_tokens without streaming raises ValueError"] — o cliente decide
# streaming internamente em vez de empurrar essa decisão para quem chama
# `chamar()`, porque é mecânica de SDK, não julgamento de conteúdo.
_LIMIAR_STREAMING_TOKENS = 16_000


@dataclass
class ResultadoDeChamada:
    texto: str
    blocos: list[dict]
    usage_bruto: dict
    model: str
    stop_reason: str | None
    veio_do_cache_local: bool
    custo_usd: float


class ClienteAnthropic:
    def __init__(
        self,
        *,
        cliente_sdk: anthropic.Anthropic | None = None,
        config: ConfiguracaoDeRobustez | None = None,
        cache: CacheLocal | None = None,
        ledger: Ledger | None = None,
        caminho_estado_prefixo: Path | None = None,
    ) -> None:
        self._config = config or ConfiguracaoDeRobustez()
        self._sdk = cliente_sdk or anthropic.Anthropic(
            max_retries=self._config.max_retries,
            timeout=self._config.timeout_segundos,
        )
        self._cache = cache or CacheLocal()
        self._ledger = ledger or Ledger()
        self._caminho_estado_prefixo = caminho_estado_prefixo
        self._estado_prefixo: EstadoPrefixo = carregar_estado_prefixo(caminho_estado_prefixo)

    def chamar(
        self,
        *,
        model: str,
        system_estavel: str,
        unidades: list[dict],
        max_tokens: int,
        effort: str,
        thinking: dict | None = None,
        tools: list[dict] | None = None,
        ttl_cache: str = "5m",
        etapa: str | None = None,
        sequence_id: str | None = None,
        indice_na_sequencia: int | None = None,
    ) -> ResultadoDeChamada:
        """Executa uma chamada de diagnóstico isolada.

        `system_estavel`: o prefixo que se repete entre chamadas da mesma
        sequência (documento + instruções fixas) — recebe `cache_control`.
        `unidades`: os blocos de conteúdo específicos desta chamada (as
        unidades de diagnóstico daquela chamada), nunca histórico acumulado.
        """
        if not effort:
            raise ErroEffortAusente()
        if not max_tokens or max_tokens <= 0:
            raise ErroMaxTokensAusente()

        mensagens = [{"role": "user", "content": unidades}]

        chave_hash = hash_requisicao(
            model=model,
            system=system_estavel,
            mensagens=mensagens,
            tools=tools,
            max_tokens=max_tokens,
            effort=effort,
            thinking=thinking,
        )

        em_cache = self._cache.obter(chave_hash)
        if em_cache is not None:
            return self._resultado_do_cache_local(
                em_cache,
                chave_hash=chave_hash,
                model=model,
                effort=effort,
                ttl_cache=ttl_cache,
                etapa=etapa,
                sequence_id=sequence_id,
                indice_na_sequencia=indice_na_sequencia,
            )

        hash_prefixo = hash_prefixo_estavel(model=model, system=system_estavel, tools=tools)
        prefixo_repetido = hash_prefixo == self._estado_prefixo.hash_prefixo

        thinking_param = thinking if thinking is not None else {"type": "adaptive"}

        system_com_cache = [
            {
                "type": "text",
                "text": system_estavel,
                "cache_control": {"type": "ephemeral", "ttl": ttl_cache},
            }
        ]

        kwargs: dict = {
            "model": model,
            "max_tokens": max_tokens,
            "system": system_com_cache,
            "messages": mensagens,
            "thinking": thinking_param,
            "output_config": {"effort": effort},
        }
        if tools:
            kwargs["tools"] = tools

        try:
            if max_tokens > _LIMIAR_STREAMING_TOKENS:
                with self._sdk.messages.stream(**kwargs) as stream:
                    resposta = stream.get_final_message()
            else:
                resposta = self._sdk.messages.create(**kwargs)
        except (anthropic.APIStatusError, anthropic.APIConnectionError) as exc:
            raise mapear_erro_sdk(exc) from exc

        usage = _usage_para_dict(resposta.usage)
        cache_read = usage["cache_read_input_tokens"] or 0
        cache_criado = usage["cache_creation_input_tokens"] or 0

        # Requisito: cache_read_input_tokens zerado em requisição de prefixo
        # idêntico aborta ANTES da próxima chamada da sequência — checagem
        # acontece aqui, logo após a resposta, não ao final da sequência.
        if prefixo_repetido and self._estado_prefixo.escreveu_cache and cache_read == 0:
            raise ErroCacheNaoAproveitado(esperado_min=1, obtido=0)

        if cache_criado:
            self._estado_prefixo = EstadoPrefixo(
                hash_prefixo=hash_prefixo, escreveu_cache=True, timestamp_unix=time.time()
            )
            salvar_estado_prefixo(self._estado_prefixo, self._caminho_estado_prefixo)
        elif not prefixo_repetido:
            # Prefixo novo mas sem escrita de cache registrada (ex.: prefixo
            # menor que o mínimo cacheável do modelo) — atualiza o hash de
            # referência sem marcar escreveu_cache.
            self._estado_prefixo = EstadoPrefixo(
                hash_prefixo=hash_prefixo, escreveu_cache=False, timestamp_unix=time.time()
            )
            salvar_estado_prefixo(self._estado_prefixo, self._caminho_estado_prefixo)

        custo = calcular_custo(
            id_modelo=model,
            input_tokens=usage["input_tokens"],
            cache_creation_input_tokens=cache_criado,
            cache_read_input_tokens=cache_read,
            output_tokens=usage["output_tokens"],
            ttl_cache=ttl_cache,
        )

        blocos = [_bloco_para_dict(bloco) for bloco in resposta.content]

        self._cache.salvar(
            chave_hash,
            RespostaCache(
                texto_blocos=blocos,
                usage=usage,
                model=resposta.model,
                stop_reason=resposta.stop_reason,
            ),
        )

        self._registrar_ledger(
            request_id=resposta.id,
            model=model,
            effort=effort,
            usage=usage,
            custo=custo,
            etapa=etapa,
            sequence_id=sequence_id,
            indice_na_sequencia=indice_na_sequencia,
            veio_do_cache_local=False,
        )

        resultado = ResultadoDeChamada(
            texto=_texto_de_blocos(blocos),
            blocos=blocos,
            usage_bruto=usage,
            model=resposta.model,
            stop_reason=resposta.stop_reason,
            veio_do_cache_local=False,
            custo_usd=custo.total,
        )
        _exigir_resposta_completa(resultado)
        return resultado

    def estimar_custo(
        self,
        *,
        model: str,
        system_estavel: str,
        unidades: list[dict],
        max_tokens: int,
        tools: list[dict] | None = None,
    ) -> float:
        """Estimativa de custo antes de executar, exibida ao chamador
        [CLAUDE.md §10]. Usa `count_tokens` (não gera resposta) e assume
        pior caso de cache (sem leitura/escrita) e output = `max_tokens` —
        teto, não previsão exata."""
        contagem = self._sdk.messages.count_tokens(
            model=model,
            system=system_estavel,
            messages=[{"role": "user", "content": unidades}],
            tools=tools or [],
        )
        custo = calcular_custo(
            id_modelo=model,
            input_tokens=contagem.input_tokens,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
            output_tokens=max_tokens,
        )
        return custo.total

    def _resultado_do_cache_local(
        self,
        em_cache: RespostaCache,
        *,
        chave_hash: str,
        model: str,
        effort: str,
        ttl_cache: str,
        etapa: str | None,
        sequence_id: str | None,
        indice_na_sequencia: int | None,
    ) -> ResultadoDeChamada:
        custo_zero = calcular_custo(
            id_modelo=model,
            input_tokens=0,
            cache_creation_input_tokens=0,
            cache_read_input_tokens=0,
            output_tokens=0,
            ttl_cache=ttl_cache,
        )
        self._registrar_ledger(
            request_id=f"cache-local:{chave_hash[:12]}",
            model=model,
            effort=effort,
            usage={
                "cache_creation_input_tokens": 0,
                "cache_read_input_tokens": 0,
                "input_tokens": 0,
                "output_tokens": 0,
            },
            custo=custo_zero,
            etapa=etapa,
            sequence_id=sequence_id,
            indice_na_sequencia=indice_na_sequencia,
            veio_do_cache_local=True,
        )
        resultado = ResultadoDeChamada(
            texto=_texto_de_blocos(em_cache.texto_blocos),
            blocos=em_cache.texto_blocos,
            usage_bruto=em_cache.usage,
            model=em_cache.model,
            stop_reason=em_cache.stop_reason,
            veio_do_cache_local=True,
            custo_usd=0.0,
        )
        _exigir_resposta_completa(resultado)
        return resultado

    def _registrar_ledger(
        self,
        *,
        request_id: str,
        model: str,
        effort: str,
        usage: dict,
        custo: CustoCalculado,
        etapa: str | None,
        sequence_id: str | None,
        indice_na_sequencia: int | None,
        veio_do_cache_local: bool,
    ) -> None:
        registro = RegistroDeCusto(
            timestamp_unix=time.time(),
            request_id=request_id,
            model=model,
            effort=effort,
            cache_creation_input_tokens=usage.get("cache_creation_input_tokens", 0) or 0,
            cache_read_input_tokens=usage.get("cache_read_input_tokens", 0) or 0,
            input_tokens=usage.get("input_tokens", 0) or 0,
            output_tokens=usage.get("output_tokens", 0) or 0,
            custo_usd_input_nao_cacheado=custo.custo_usd_input_nao_cacheado,
            custo_usd_escrita_cache=custo.custo_usd_escrita_cache,
            custo_usd_leitura_cache=custo.custo_usd_leitura_cache,
            custo_usd_output=custo.custo_usd_output,
            custo_usd_total=custo.total,
            veio_do_cache_local=veio_do_cache_local,
            etapa=etapa,
            sequence_id=sequence_id,
            indice_na_sequencia=indice_na_sequencia,
        )
        self._ledger.registrar(registro)


def _exigir_resposta_completa(resultado: ResultadoDeChamada) -> None:
    """`stop_reason == "max_tokens"` nunca é resultado válido — regra do
    cliente, não de uma ponte específica [`ErroRespostaTruncada`].
    Verificada nos dois caminhos de `chamar()` (chamada real e cache
    local), para que nenhum chamador (`ponte_modelo_p13.py`,
    `ponte_modelo_p11.py`, ou qualquer ponte futura) precise repetir esta
    checagem por conta própria."""
    if resultado.stop_reason == "max_tokens":
        raise ErroRespostaTruncada(resultado.model)


def _usage_para_dict(usage: object) -> dict:
    return {
        "input_tokens": getattr(usage, "input_tokens", 0) or 0,
        "output_tokens": getattr(usage, "output_tokens", 0) or 0,
        "cache_creation_input_tokens": getattr(usage, "cache_creation_input_tokens", 0) or 0,
        "cache_read_input_tokens": getattr(usage, "cache_read_input_tokens", 0) or 0,
    }


def _bloco_para_dict(bloco: object) -> dict:
    if isinstance(bloco, dict):
        return bloco
    if hasattr(bloco, "model_dump"):
        return bloco.model_dump()
    return {"type": getattr(bloco, "type", None), "text": getattr(bloco, "text", None)}


def _texto_de_blocos(blocos: list[dict]) -> str:
    return "".join(bloco.get("text", "") for bloco in blocos if bloco.get("type") == "text")
