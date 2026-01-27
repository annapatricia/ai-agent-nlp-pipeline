import json
import os
from typing import Dict, Any, Optional

from openai import OpenAI
from src.prompts import EXTRACTION_INSTRUCTIONS


def _has_api_key() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def llm_extract(texto: str, model: str = "gpt-5.2") -> Optional[Dict[str, Any]]:
    """
    Extrai campos via LLM e retorna dict.
    Se não houver OPENAI_API_KEY, retorna None (para o agente usar fallback de regras).
    """
    if not _has_api_key():
        return None

    client = OpenAI()

    # Quickstart: client.responses.create(model=..., input=...) :contentReference[oaicite:2]{index=2}
    response = client.responses.create(
        model=model,
        input=texto,
        instructions=EXTRACTION_INSTRUCTIONS,
    )

    # O SDK expõe output_text no quickstart :contentReference[oaicite:3]{index=3}
    raw = (response.output_text or "").strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # Se o modelo devolveu algo fora do JSON, falha com fallback
        return None

    # Validação mínima para evitar lixo
    required = {"categoria", "data", "valor", "protocolo"}
    if not isinstance(data, dict) or not required.issubset(set(data.keys())):
        return None

    return data
