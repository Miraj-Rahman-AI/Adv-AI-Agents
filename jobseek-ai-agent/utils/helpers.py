import re
import uuid
from typing import List


def generate_id() -> str:
    """Generate a unique ID."""
    return str(uuid.uuid4())


def clean_text(text: str) -> str:
    """Normalize whitespace."""
    if not text:
        return ""
    return " ".join(text.split()).strip()


def extract_numbers(text: str) -> List[str]:
    """Extract numbers from text."""
    return re.findall(r"\d+", text)


def safe_get(dictionary, key, default=""):
    """Safely get value from dictionary."""
    return dictionary.get(key, default) if dictionary else default
