import pytest
from schemaguard.validator import validate_fields, validate_types, check_missing, check_duplicates, validate
from schemaguard.schema import load_schema

@pytest.fixture
def sample_data():
    return [
        {"id": "1", "name": "Alice", "email": "alice@example.invalid", "phone": "555-0001", "created_at": "2024-01-01T00:00:00Z"}
    ]

def test_validate_fields_all_present(sample_schema):
    schema = load_schema(sample_schema)
    headers = ["id", "name", "email", "phone", "created_at"]
    errors = validate_fields(headers, schema)
    assert len(errors) == 0

def test_validate_fields_missing(sample_schema):
    schema = load_schema(sample_schema)
    headers = ["id", "name"]
    errors = validate_fields(headers, schema)
    assert len(errors) > 0

def test_validate_types_valid(sample_schema, sample_data):
    schema = load_schema(sample_schema)
    errors = validate_types(sample_data, schema)
    assert len(errors) == 0

def test_validate_types_invalid(sample_schema):
    schema = load_schema(sample_schema)
    data = [{"id": "not_an_int", "name": "Alice", "email": "alice@example.invalid", "phone": "555-0001", "created_at": "2024-01-01T00:00:00Z"}]
    errors = validate_types(data, schema)
    assert len(errors) > 0

def test_check_missing_none(sample_schema, sample_data):
    schema = load_schema(sample_schema)
    missing = check_missing(sample_data, schema)
    assert missing["name"]["missing_count"] == 0

def test_check_missing_some(sample_schema):
    schema = load_schema(sample_schema)
    data = [{"id": "1", "name": ""}]
    missing = check_missing(data, schema)
    assert missing["name"]["missing_count"] == 1

def test_check_duplicates_none(sample_schema, sample_data):
    schema = load_schema(sample_schema)
    dups = check_duplicates(sample_data, schema)
    assert len(dups) == 0

def test_check_duplicates_exact(sample_schema, sample_data):
    schema = load_schema(sample_schema)
    data = sample_data + sample_data
    dups = check_duplicates(data, schema)
    assert len(dups) == 1

def test_validate_full(sample_schema, sample_data):
    schema = load_schema(sample_schema)
    headers = ["id", "name", "email", "phone", "created_at"]
    report = validate(headers, sample_data, schema)
    assert len(report["field_errors"]) == 0
    assert len(report["type_errors"]) == 0
