import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

def generate_report(filepath: Path, headers: List[str], rows: List[Dict[str, Any]], schema: Optional[Dict[str, Any]] = None, validation_result: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Generate a comprehensive JSON report."""
    row_count = len(rows)
    column_count = len(headers)
    
    columns_info = []
    for h in headers:
        missing = sum(1 for r in rows if not r.get(h))
        columns_info.append({
            "name": h,
            "inferred_type": "string",
            "missing_count": missing
        })
        
    is_valid = True
    error_locations = []
    
    if validation_result:
        if validation_result.get("field_errors") or validation_result.get("type_errors"):
            is_valid = False
            
        for err in validation_result.get("field_errors", []):
            error_locations.append({"row": None, "column": err.get("field"), "error_type": err.get("error_type"), "message": "Missing required field"})
            
        for err in validation_result.get("type_errors", []):
            error_locations.append({"row": err.get("row"), "column": err.get("field"), "error_type": err.get("expected_type"), "message": f"Expected {err.get('expected_type')}, got {err.get('actual_value')}"})
    
    report = {
        "file": str(filepath),
        "valid": is_valid,
        "row_count": row_count,
        "column_count": column_count,
        "columns": columns_info,
        "rule_results": validation_result if validation_result else {},
        "error_locations": error_locations,
        "summary": "Report generated successfully.",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    return report

def save_report(report: Dict[str, Any], output_path: Path):
    """Save report as JSON."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

def format_summary(report: Dict[str, Any]) -> str:
    """Human-readable summary string."""
    lines = [
        f"File: {report['file']}",
        f"Valid: {report['valid']}",
        f"Rows: {report['row_count']}, Columns: {report['column_count']}",
        f"Generated At: {report['timestamp']}"
    ]
    return "\n".join(lines)
