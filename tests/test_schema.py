import pytest
from schemaguard.errors import SchemaError
from schemaguard.schema import load_schema, validate_schema

def test_load_schema(sample_schema):
    schema = load_schema(sample_schema)
    assert "fields" in schema
    assert schema["settings"]["duplicate_check"] == "exact"

def test_load_schema_invalid_path():
    with pytest.raises(SchemaError):
        load_schema("nonexistent_schema.yml")

def test_validate_schema_valid(sample_schema):
    schema = load_schema(sample_schema)
    validate_schema(schema)

def test_validate_schema_missing_fields():
    schema = {"settings": {}}
    with pytest.raises(SchemaError):
        validate_schema(schema)

def test_validate_schema_invalid_type(sample_schema):
    schema = load_schema(sample_schema)
    schema["fields"][0]["type"] = "unsupported_type"
    with pytest.raises(SchemaError):
        validate_schema(schema)
