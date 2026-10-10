import csv
import json
from pathlib import Path
from typing import Tuple, List, Dict, Any
from .errors import FileReadError

def read_csv(filepath: Path) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Read CSV, return (headers, rows as list of dicts)."""
    filepath = Path(filepath)
    try:
        if filepath.exists() and filepath.stat().st_size == 0:
            raise FileReadError("File is empty")
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                return [], []
            headers = list(reader.fieldnames)
            rows = list(reader)
            return headers, rows
    except FileReadError:
        raise
    except Exception as e:
        raise FileReadError(f"Failed to read CSV file {filepath}: {e}")

def read_json(filepath: Path) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Read JSON array of objects, return headers and rows."""
    filepath = Path(filepath)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("JSON root must be an array of objects")
            if not data:
                return [], []
            headers = list(data[0].keys())
            return headers, data
    except Exception as e:
        raise FileReadError(f"Failed to read JSON file {filepath}: {e}")

def read_file(filepath: Path) -> Tuple[List[str], List[Dict[str, Any]]]:
    """Auto-detect format by extension, dispatch to csv/json reader."""
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileReadError(f"File not found: {filepath}")
    
    suffix = filepath.suffix.lower()
    if suffix == '.csv':
        return read_csv(filepath)
    elif suffix == '.json':
        return read_json(filepath)
    else:
        raise FileReadError(f"Unsupported file format: {suffix}")
