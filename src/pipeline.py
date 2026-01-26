import os
import re
from typing import List, Dict

def load_texts(path: str) -> List[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines()]

    # remove linhas vazias
    return [ln for ln in lines if ln]


def normalize_text(text: str) -> str:
    # normaliza espaços e remove duplicações simples
    text = re.sub(r"\s+", " ", text).strip()
    return text


def preprocess(texts: List[str]) -> List[str]:
    return [normalize_text(t) for t in texts]


def build_records(texts: List[str]) -> List[Dict]:
    """
    Estrutura registros iniciais com id e texto.
    """
    records = []
    for i, t in enumerate(texts, start=1):
        records.append({"id": i, "texto": t})
    return records
