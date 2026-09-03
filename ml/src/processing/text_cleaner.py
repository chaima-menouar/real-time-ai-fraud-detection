import hashlib
import re
import unicodedata

URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b")
PHONE_PATTERN = re.compile(r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)")
WHITESPACE_PATTERN = re.compile(r"\s+")


def clean_text(value: object) -> str:
    text = unicodedata.normalize("NFKC", str(value or ""))
    text = URL_PATTERN.sub("[URL]", text)
    text = EMAIL_PATTERN.sub("[EMAIL]", text)
    text = PHONE_PATTERN.sub("[PHONE]", text)
    return WHITESPACE_PATTERN.sub(" ", text).strip()


def normalized_group_id(text: str) -> str:
    canonical = clean_text(text).casefold()
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
