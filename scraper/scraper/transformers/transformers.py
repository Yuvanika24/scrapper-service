import re

def to_float(value):
    if not value:
        return None
    cleaned = re.sub(r"[^\d.-]+", "", value)
    try:
        return float(cleaned)
    except ValueError:
        return None

def text_clean(value):
    if isinstance(value, str):
        return value.replace("\n", " ").replace("\r", " ").strip()
    return value

TRANSFORMER_FUNCTIONS = {
    "to_float": to_float,
    "text_clean": text_clean,
}
