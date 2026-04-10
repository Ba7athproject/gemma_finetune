# scripts/validate_examples.py
from pathlib import Path
from pydantic import ValidationError
from schemas.osint import OSINTDocument

def main():
    example_path = Path("data/processed/example_osint.json")
    if not example_path.exists():
        raise SystemExit(f"{example_path} n'existe pas encore.")
    data = example_path.read_text(encoding="utf-8")
    try:
        obj = OSINTDocument.model_validate_json(data)
        print("OK: JSON valide selon OSINTDocument")
        print("document_id:", obj.document_id)
    except ValidationError as e:
        print("ERREUR de validation:")
        print(e)

if __name__ == "__main__":
    main()