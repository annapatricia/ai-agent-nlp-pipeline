#orquestra e gera saida em json
import json
import os
from typing import Dict, Any

from pipeline import load_texts, preprocess, build_records
from nlp import extract

INPUT_PATH = "data/raw/textos.txt"
OUTPUT_PATH = "outputs/extractions.json"

def run_agent(input_path: str = INPUT_PATH, output_path: str = OUTPUT_PATH) -> Dict[str, Any]:
    textos = load_texts(input_path)
    textos = preprocess(textos)

    records = build_records(textos)

    enriched = []
    for r in records:
        info = extract(r["texto"])
        enriched.append({**r, **info})

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)

    summary = {
        "total_registros": len(enriched),
        "output_path": output_path
    }
    return summary


if __name__ == "__main__":
    result = run_agent()
    print("OK:", result)
