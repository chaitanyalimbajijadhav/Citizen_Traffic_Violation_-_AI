import re


PLATE_PATTERN = re.compile(r"^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$")


def normalize_plate_text(raw_text: str) -> str:
    if raw_text is None:
        return ""

    cleaned = str(raw_text).strip().upper()
    cleaned = re.sub(r"[^A-Z0-9]", "", cleaned)
    return cleaned


def is_valid_indian_plate_format(plate_text: str) -> bool:
    normalized = normalize_plate_text(plate_text)
    if not normalized:
        return False
    return bool(PLATE_PATTERN.fullmatch(normalized))
