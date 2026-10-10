import json
import pytest
import yaml
from pathlib import Path

@pytest.fixture
def tmp_csv(tmp_path):
    file_path = tmp_path / "data.csv"
    content = """id,name,email,phone,created_at
1,Alice,alice@example.invalid,555-0001,2024-01-01T00:00:00+00:00
2,Bob,bob@example.invalid,555-0002,2024-01-02T00:00:00+00:00
3,Charlie,charlie@example.invalid,555-0003,2024-01-03T00:00:00+00:00
"""
    file_path.write_text(content, encoding="utf-8")
    return file_path

@pytest.fixture
def tmp_json(tmp_path):
    file_path = tmp_path / "data.json"
    data = [
        {"id": 1, "name": "Alice", "email": "alice@example.invalid", "phone": "555-0001", "created_at": "2024-01-01T00:00:00+00:00"},
        {"id": 2, "name": "Bob", "email": "bob@example.invalid", "phone": "555-0002", "created_at": "2024-01-02T00:00:00+00:00"},
        {"id": 3, "name": "Charlie", "email": "charlie@example.invalid", "phone": "555-0003", "created_at": "2024-01-03T00:00:00+00:00"}
    ]
    file_path.write_text(json.dumps(data), encoding="utf-8")
    return file_path

@pytest.fixture
def tmp_csv_bom(tmp_path):
    file_path = tmp_path / "data_bom.csv"
    content = """id,name,email,phone,created_at
1,Alice,alice@example.invalid,555-0001,2024-01-01
"""
    with open(file_path, "wb") as f:
        f.write(b'\xef\xbb\xbf')
        f.write(content.encode("utf-8"))
    return file_path

@pytest.fixture
def tmp_csv_empty(tmp_path):
    file_path = tmp_path / "empty.csv"
    file_path.write_text("", encoding="utf-8")
    return file_path

@pytest.fixture
def tmp_csv_headers_only(tmp_path):
    file_path = tmp_path / "headers_only.csv"
    file_path.write_text("id,name,email,phone,created_at\n", encoding="utf-8")
    return file_path

@pytest.fixture
def sample_schema(tmp_path):
    file_path = tmp_path / "schema.yml"
    schema = {
        "fields": [
            {"name": "id", "type": "int", "required": True},
            {"name": "name", "type": "string", "required": True},
            {"name": "email", "type": "string", "required": True},
            {"name": "phone", "type": "string", "required": True},
            {"name": "created_at", "type": "date", "required": True}
        ],
        "settings": {
            "duplicate_check": "exact",
            "date_format": "%Y-%m-%d"
        }
    }
    file_path.write_text(yaml.dump(schema), encoding="utf-8")
    return str(file_path)

@pytest.fixture
def sample_schema_normalized(tmp_path):
    file_path = tmp_path / "schema_normalized.yml"
    schema = {
        "fields": [
            {"name": "id", "type": "int", "required": True},
            {"name": "name", "type": "string", "required": True},
            {"name": "email", "type": "string", "required": True},
            {"name": "phone", "type": "string", "required": True},
            {"name": "created_at", "type": "date", "required": True}
        ],
        "settings": {
            "duplicate_check": "normalized",
            "date_format": "%Y-%m-%d"
        }
    }
    file_path.write_text(yaml.dump(schema), encoding="utf-8")
    return str(file_path)
