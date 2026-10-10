# SchemaGuard

![CI](https://img.shields.io/badge/CI-passing-brightgreen) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.11+-blue)

A data quality inspection and privacy redaction CLI tool for CSV and JSON data.

> **Note**: This repository is a synthetic benchmark created for evaluating RepoCare.
> Its issues and pull requests are intentionally designed test cases.
> They do not represent real community reports or external maintainer adoption.

## Features
- CSV/JSON reading
- Schema validation
- PII detection & redaction
- Quality reporting
- Data comparison

## Installation
```bash
pip install -e .
pip install -e '.[dev]'
```

## Quick Start
```bash
# Inspect data
schemaguard inspect data.csv

# Validate data
schemaguard validate data.csv schema.yml

# Redact PII
schemaguard redact data.json -o clean.json

# Generate quality report
schemaguard report data.csv report.md

# Compare datasets
schemaguard compare old.json new.json
```

## Testing
```bash
python -m pytest
```

## Limitations
- Not a database tool
- No network access
- Limited PII patterns
- Not a compliance scanner

## Security & Privacy
No network access or real user data is collected or sent anywhere. All tests must use fictitious samples.

## License
MIT
