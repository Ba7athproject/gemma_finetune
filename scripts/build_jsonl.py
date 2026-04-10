import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from schemas.osint import OSINTDocument

SYSTEM_PROMPT = (
    "Tu es un assistant OSINT. Tu dois analyser des documents et produire "
    "UNIQUEMENT un JSON valide respectant strictement le schéma OSINTDocument. "
    "N'invente pas d'entités, de dates ou d'événements qui ne sont pas mentionnés. "
    "Utilise la valeur 'unknown' quand nécessaire, ou laisse les listes vides si l'information manque."
)


def build_example(document_text: str, osint_json: str) -> dict:
    obj = OSINTDocument.model_validate_json(osint_json)

    return {
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    "Analyse ce document et renvoie: sources, entités, "
                    "évaluation de crédibilité, red flags, classification, "
                    "au format JSON.\n\nDocument:\n" + document_text
                ),
            },
            {
                "role": "assistant",
                "content": obj.model_dump_json(ensure_ascii=False),
            },
        ]
    }


def main():
    raw_dir = ROOT / "data" / "raw"
    labels_dir = ROOT / "data" / "processed" / "labels"
    output_path = ROOT / "data" / "processed" / "train_osint.jsonl"

    if not raw_dir.exists():
        raise SystemExit(f"Dossier introuvable: {raw_dir}")

    if not labels_dir.exists():
        raise SystemExit(f"Dossier introuvable: {labels_dir}")

    examples = []

    for txt_path in sorted(raw_dir.glob("doc_*.txt")):
        json_path = labels_dir / f"{txt_path.stem}.json"

        if not json_path.exists():
            print(f"[WARN] Label manquant pour {txt_path.name} -> {json_path.name}")
            continue

        document_text = txt_path.read_text(encoding="utf-8").strip()
        osint_json = json_path.read_text(encoding="utf-8")

        if not document_text:
            print(f"[WARN] Texte vide: {txt_path.name}")
            continue

        example = build_example(document_text, osint_json)
        examples.append(example)

    if not examples:
        raise SystemExit("Aucun exemple valide trouvé. Vérifie data/raw et data/processed/labels.")

    with output_path.open("w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")

    print(f"OK: {len(examples)} exemple(s) écrit(s) dans {output_path}")


if __name__ == "__main__":
    main()