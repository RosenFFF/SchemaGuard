# SchemaGuard Project Specification

## Overview
- **Project name:** SchemaGuard
- **Purpose:** Data quality inspection and privacy redaction CLI tool for CSV/JSON data.
- **Python version:** 3.11+

## Commands and CLI Spec
- `schemaguard inspect FILE` - Show field names, types, row count, missing values summary.
- `schemaguard validate FILE --schema schema.yml` - Validate data against a YAML schema definition.
- `schemaguard redact FILE --fields email,phone` - Redact specified PII fields, output cleaned copy.
- `schemaguard report FILE --output report.json` - Generate a JSON quality report.
- `schemaguard compare BEFORE AFTER` - Compare two files for structural/content differences.

## Exit Codes
- `0` = Success
- `1` = Validation failure
- `2` = Input error (file not found, unreadable)
- `3` = Schema error

## Inputs and Outputs
- **Input formats:** CSV (UTF-8, UTF-8 BOM), JSON (array of objects).
- **Output:** JSON reports, redacted CSV/JSON copies.

## Non-goals
- Not a database tool.
- Not a full privacy compliance scanner.
- No network access.
- No real-time monitoring.

## Security Boundaries
- Only reads user-specified files.
- No arbitrary shell execution.
- Fictitious test data only.
- No real keys.

## License
- MIT

## Technical Constraints and Behavior
- **Date format:** ISO-8601, timezone-aware dates compared as UTC, timezone-naive dates rejected or require explicit timezone.
- **Redaction:** Creates new copy, never overwrites original, preserves column and row order.
- **PII detection:** Explicit field-based redaction + limited regex hints, not automatic full-content rewriting.
- **Type checking:** string, int, float, date; no silent data replacement.
- **Duplicate detection:** Default exact match; configurable case-insensitive/whitespace-normalized mode.
- **Report format:** Contains `valid` boolean, `row_count`, `column_count`, `rule_results` array, `error_locations` with row/column.
