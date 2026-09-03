from app.labels import is_risk_label, normalize_label


def test_normal_label_is_not_risky():
    assert normalize_label(" Normal ") == "normal"
    assert is_risk_label("normal") is False


def test_specific_category_is_preserved_and_risky():
    assert normalize_label("Identity Fraud") == "identity_fraud"
    assert is_risk_label("Identity Fraud") is True
