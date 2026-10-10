import yaml
from pathlib import Path
from typing import Dict, Any
from .errors import SchemaError

def load_schema(filepath: Path) -> Dict[str, Any]:
    """Load a YAML schema file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            schema = yaml.safe_load(f)
        validate_schema(schema)
        return schema
    except SchemaError:
        raise
    except Exception as e:
        raise SchemaError(f"Failed to load schema from {filepath}: {e}")

def validate_schema(schema: Dict[str, Any]) -> None:
    """Validate the schema structure itself."""
    if not isinstance(schema, dict):
        raise SchemaError("Schema must be a dictionary")
    if 'fields' not in schema or not isinstance(schema['fields'], list):
        raise SchemaError("Missing or invalid 'fields' in schema")
    
    valid_types = {'string', 'int', 'float', 'date'}
    for field in schema['fields']:
        if 'name' not in field:
            raise SchemaError("Field missing 'name'")
        if 'type' not in field:
            raise SchemaError("Field missing 'type'")
        if field['type'] not in valid_types:
            raise SchemaError(f"Invalid type: {field['type']}")
