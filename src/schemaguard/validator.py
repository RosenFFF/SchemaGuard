from typing import List, Dict, Any
from datetime import datetime
from .errors import ValidationError

def validate_fields(headers: List[str], schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check all required fields exist."""
    errors = []
    required_fields = [f['name'] for f in schema.get('fields', []) if f.get('required', False)]
    for req_field in required_fields:
        if req_field not in headers:
            errors.append({"field": req_field, "error_type": "missing_required_field"})
    return errors

def validate_types(rows: List[Dict[str, Any]], schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Check each cell matches expected type."""
    errors = []
    field_types = {f['name']: f['type'] for f in schema.get('fields', [])}
    
    for i, row in enumerate(rows):
        for field, expected_type in field_types.items():
            val = row.get(field)
            if val is None or val == "":
                continue
            
            if expected_type == 'int':
                try:
                    int(val)
                except ValueError:
                    errors.append({"row": i, "field": field, "expected_type": "int", "actual_value": val})
            elif expected_type == 'date':
                try:
                    dt = datetime.fromisoformat(str(val))
                    if dt.tzinfo is None:
                        errors.append({
                            "row": i, "field": field, "expected_type": "date_with_tz",
                            "actual_value": val, "message": "timezone is required"
                        })
                except ValueError:
                    errors.append({"row": i, "field": field, "expected_type": "date", "actual_value": val})
                    
    return errors

def check_missing(rows: List[Dict[str, Any]], schema: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Count missing/null/empty values per field."""
    fields = [f['name'] for f in schema.get('fields', [])]
    total = len(rows)
    result = {}
    for field in fields:
        missing_count = sum(1 for row in rows if not row.get(field))
        pct = (missing_count / total * 100) if total > 0 else 0
        result[field] = {"missing_count": missing_count, "total": total, "percentage": pct}
    return result

def check_duplicates(rows: List[Dict[str, Any]], schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Find duplicate rows."""
    dup_check_type = schema.get('settings', {}).get('duplicate_check', 'exact')
    seen = {}
    duplicates = []
    
    for i, row in enumerate(rows):
        if dup_check_type == 'normalized':
            norm_row = tuple((str(v).strip().lower() if v is not None else "") for k, v in row.items())
        else:
            norm_row = tuple((str(v) if v is not None else "") for k, v in row.items())
        
        if norm_row in seen:
            seen[norm_row].append(i)
        else:
            seen[norm_row] = [i]
            
    for group in seen.values():
        if len(group) > 1:
            duplicates.append({"row_indices": group})
    return duplicates

def validate(headers: List[str], rows: List[Dict[str, Any]], schema: Dict[str, Any]) -> Dict[str, Any]:
    """Run all validations, return full result dict."""
    return {
        "field_errors": validate_fields(headers, schema),
        "type_errors": validate_types(rows, schema),
        "missing": check_missing(rows, schema),
        "duplicates": check_duplicates(rows, schema)
    }
