import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pydantic import ValidationError
from schemas.osint import OSINTDocument


def main():
    example_path = ROOT / "data" / "processed" / "labels" / "doc_0001.json"

    if not example_path.exists():
        raise SystemExit(f"{example_path} n'existe pas encore.")

    data = example_path.read_text(encoding="utf-8")

    try:
        obj = OSINTDocument.model_validate_json(data)
        print("OK: JSON valide selon OSINTDocument")
        print("document_id:", obj.document_id)
        print("source_type:", obj.source_type)
        print("claims:", len(obj.claims))
    except ValidationError as e:
        print("ERREUR de validation:")
        print(e)


if __name__ == "__main__":
    main()