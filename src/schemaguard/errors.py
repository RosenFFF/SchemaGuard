class SchemaGuardError(Exception):
    """Base exception for SchemaGuard."""
    pass

class FileReadError(SchemaGuardError):
    """File reading errors (exit code 2)."""
    pass

class SchemaError(SchemaGuardError):
    """Schema definition errors (exit code 3)."""
    pass

class ValidationError(SchemaGuardError):
    """Data validation errors (exit code 1)."""
    pass

class RedactionError(SchemaGuardError):
    """Redaction processing errors."""
    pass
