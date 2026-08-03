"""Serialização da estrutura canônica para JSON — formato documentado em
escolio/ingestao/FORMATO.md."""

import dataclasses
import json

from escolio.ingestao.modelos import DocumentoIngerido


def _padrao(obj):
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        d = dataclasses.asdict(obj)
        return d
    if hasattr(obj, "value"):  # Enum
        return obj.value
    raise TypeError(f"Objeto não serializável: {type(obj)!r}")


def documento_para_dict(doc: DocumentoIngerido) -> dict:
    bruto = dataclasses.asdict(doc)
    return bruto


def documento_para_json(doc: DocumentoIngerido, indent: int = 2) -> str:
    return json.dumps(documento_para_dict(doc), ensure_ascii=False, indent=indent, default=_padrao)
