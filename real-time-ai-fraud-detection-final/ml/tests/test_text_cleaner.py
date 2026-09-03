from src.processing.text_cleaner import clean_text, normalized_group_id


def test_sensitive_patterns_are_redacted():
    text = clean_text("mail me at user@example.com or https://bad.example and +212 600 000 000")
    assert "[EMAIL]" in text
    assert "[URL]" in text
    assert "[PHONE]" in text
    assert "example.com" not in text


def test_group_id_is_case_and_space_stable():
    assert normalized_group_id(" Same   text ") == normalized_group_id("same text")
