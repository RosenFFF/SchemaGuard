# File Format Specification

## CSV
- **Encoding**: UTF-8 and UTF-8 with BOM support.
- **Delimiter**: Comma (`,`).
- **Quoting**: Standard quoted fields are supported.

## JSON
- **Structure**: Must be an array of objects.
- **Encoding**: UTF-8.

## Type Handling Rules
- **string**: Processed as standard string fields.
- **int**: Parsed as integers.
- **float**: Parsed as floating-point numbers.
- **date**: Processed as dates.

## Null/Empty/Whitespace Handling Rules
- Empty strings and pure whitespace are treated as such, unless defined otherwise by the schema.
- JSON `null` values are mapped to appropriate empty/none representations.

## Date Format
- Dates must follow the ISO-8601 standard.

## Data Preservation
- **No silent data replacement policy**: The tool will not silently replace data unless explicitly instructed via the redaction command.
