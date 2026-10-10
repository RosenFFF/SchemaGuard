import pytest
from schemaguard.errors import FileReadError
from schemaguard.reader import read_csv, read_json, read_file

def test_read_csv_basic(tmp_csv):
    headers, rows = read_csv(str(tmp_csv))
    assert headers == ["id", "name", "email", "phone", "created_at"]
    assert len(rows) == 3

def test_read_csv_content(tmp_csv):
    headers, rows = read_csv(str(tmp_csv))
    assert rows[0]["name"] == "Alice"
    assert rows[1]["email"] == "bob@example.invalid"

def test_read_json_basic(tmp_json):
    headers, rows = read_json(str(tmp_json))
    assert "id" in headers
    assert len(rows) == 3

def test_read_json_content(tmp_json):
    headers, rows = read_json(str(tmp_json))
    assert rows[0]["name"] == "Alice"
    assert rows[2]["phone"] == "555-0003"

def test_read_file_csv(tmp_csv):
    headers, rows = read_file(str(tmp_csv))
    assert len(rows) == 3

def test_read_file_json(tmp_json):
    headers, rows = read_file(str(tmp_json))
    assert len(rows) == 3

def test_read_file_not_found():
    with pytest.raises(FileReadError):
        read_file("nonexistent.csv")

def test_read_csv_empty(tmp_csv_empty):
    with pytest.raises(FileReadError):
        read_csv(str(tmp_csv_empty))

def test_read_csv_headers_only(tmp_csv_headers_only):
    headers, rows = read_csv(str(tmp_csv_headers_only))
    assert headers == ["id", "name", "email", "phone", "created_at"]
    assert len(rows) == 0

def test_read_csv_bom(tmp_csv_bom):
    headers, rows = read_csv(str(tmp_csv_bom))
    assert len(headers) > 0
    assert len(rows) == 1
