from schemaguard.pii import detect_pii_fields, detect_pii_values, redact_value, redact_rows

def test_detect_pii_fields():
    fields = ["id", "name", "email", "phone_number", "address"]
    pii = detect_pii_fields(fields)
    assert "email" in pii
    assert "phone_number" in pii

def test_detect_pii_fields_none():
    fields = ["id", "amount", "date"]
    assert len(detect_pii_fields(fields)) == 0

def test_detect_pii_values_email():
    assert len(detect_pii_values("contact bob@example.invalid today")) > 0

def test_detect_pii_values_phone():
    assert len(detect_pii_values("call 555-555-1234 for details")) > 0

def test_detect_pii_values_none():
    assert len(detect_pii_values("hello world")) == 0

def test_redact_value_mask():
    assert redact_value("bob@example.invalid", "email") == "***REDACTED***"

def test_redact_rows():
    rows = [
        {"id": "1", "email": "alice@example.invalid", "name": "Alice"},
        {"id": "2", "email": "bob@example.invalid", "name": "Bob"}
    ]
    redacted = redact_rows(rows, ["email"])
    assert redacted[0]["email"] == "***REDACTED***"
    assert redacted[1]["email"] == "***REDACTED***"
    assert redacted[0]["name"] == "Alice"
