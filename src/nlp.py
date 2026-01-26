#extração simples de informações

import re
from typing import Dict

# Regras simples (baseline) para extração
RE_DATA = re.compile(r"\b(\d{2}/\d{2}/\d{4})\b")
RE_VALOR = re.compile(r"R\$\s*([\d\.]+,\d{2})")
RE_PROTOCOLO = re.compile(r"\bprotocolo\s*(\d+)\b", re.IGNORECASE)

CATEGORIAS = [
    ("compra_não_reconhecida", ["compra não reconhecida", "não reconhecida", "fraude"]),
    ("cartão_bloqueado", ["cartão foi bloqueado", "cartão bloqueado", "bloqueado"]),
    ("aumento_limite", ["aumento de limite", "limite"]),
    ("cobrança_duplicada", ["cobrança duplicada", "duplicada"]),
    ("entrega_cartão", ["cartão não chegou", "não chegou", "entrega"]),
]

def classify(texto: str) -> str:
    t = texto.lower()
    for cat, keywords in CATEGORIAS:
        if any(k in t for k in keywords):
            return cat
    return "outros"


def extract(texto: str) -> Dict:
    data = RE_DATA.search(texto)
    valor = RE_VALOR.search(texto)
    protocolo = RE_PROTOCOLO.search(texto)

    return {
        "categoria": classify(texto),
        "data": data.group(1) if data else None,
        "valor": valor.group(1) if valor else None,
        "protocolo": protocolo.group(1) if protocolo else None,
    }
