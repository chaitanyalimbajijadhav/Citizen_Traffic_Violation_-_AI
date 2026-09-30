import re


def normalize_plate_text(raw_text: str) -> str:
    if raw_text is None:
        return ""

    cleaned = str(raw_text).strip().upper()
    cleaned = re.sub(r"[^A-Z0-9]", "", cleaned)
    return cleaned
