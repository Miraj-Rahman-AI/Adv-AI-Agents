import json
import csv
from pathlib import Path
from typing import List, Dict


def ensure_directory(path: str):
    """Create directory if it does not exist."""
    Path(path).mkdir(parents=True, exist_ok=True)


def read_json(file_path: str):
    """Read JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(data, file_path: str):
    """Write JSON file."""
    ensure_directory(Path(file_path).parent)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def write_csv(data: List[Dict], file_path: str):
    """Write CSV file."""
    if not data:
        return

    ensure_directory(Path(file_path).parent)

    keys = data[0].keys()

    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def read_text(file_path: str) -> str:
    """Read text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def write_text(content: str, file_path: str):
    """Write text file."""
    ensure_directory(Path(file_path).parent)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
