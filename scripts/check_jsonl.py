import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    path = ROOT / "data" / "processed" / "train_osint.jsonl"

    if not path.exists():
        raise SystemExit(f"Fichier introuvable: {path}")

    lines = path.read_text(encoding="utf-8").splitlines()

    print(f"Lignes: {len(lines)}")

    for i, line in enumerate(lines, start=1):
        obj = json.loads(line)
        assert "messages" in obj, f"Ligne {i}: clé 'messages' absente"
        assert isinstance(obj["messages"], list), f"Ligne {i}: 'messages' doit être une liste"
        print(f"Ligne {i}: OK")

    print("JSONL valide")
    

if __name__ == "__main__":
    main()