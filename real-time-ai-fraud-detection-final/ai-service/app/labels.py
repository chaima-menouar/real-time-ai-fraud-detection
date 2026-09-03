NORMAL_LABELS = {"normal", "legitimate", "safe", "no_fraud", "non_fraud", "non-fraud"}


def normalize_label(label: str) -> str:
    """Return a stable API label without collapsing the original category."""
    normalized = label.strip().lower().replace(" ", "_")
    return normalized or "unknown"


def is_risk_label(label: str) -> bool:
    return normalize_label(label) not in NORMAL_LABELS
