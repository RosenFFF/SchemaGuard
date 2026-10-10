import re
import hashlib
from typing import List, Dict, Any
from .errors import RedactionError

def detect_pii_fields(headers: List[str]) -> List[str]:
    """Detect fields that likely contain PII based on field names."""
    pii_keywords = {'email', 'phone', 'name', 'address', 'ssn', 'password'}
    detected = []
    for h in headers:
        if any(kw in h.lower() for kw in pii_keywords):
            detected.append(h)
    return detected

def detect_pii_values(value: str) -> List[str]:
    """Detect PII patterns in values using regex."""
    detected = []
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    if re.search(email_pattern, str(value)):
        detected.append('email')
        
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    if re.search(phone_pattern, str(value)):
        detected.append('phone')
        
    return detected

def redact_value(value: str, field: str, method: str = 'mask') -> str:
    """Redact a value."""
    if not value:
        return value
    if method == 'mask':
        return '***REDACTED***'
    elif method == 'hash':
        return hashlib.sha256(str(value).encode('utf-8')).hexdigest()
    else:
        raise RedactionError(f"Unknown redaction method: {method}")

def redact_rows(rows: List[Dict[str, Any]], fields: List[str], method: str = 'mask') -> List[Dict[str, Any]]:
    """Redact specified fields in all rows."""
    redacted_rows = []
    for row in rows:
        new_row = {}
        # Defect: puts redacted fields first, mutating column order
        for f in fields:
            if f in row and row[f]:
                new_row[f] = redact_value(row[f], f, method)
        for k, v in row.items():
            if k not in fields:
                new_row[k] = v
        redacted_rows.append(new_row)
    return redacted_rows
