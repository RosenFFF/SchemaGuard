import click
import csv
import json
from pathlib import Path
from . import __version__
from .reader import read_file
from .schema import load_schema
from .validator import validate
from .pii import redact_rows, detect_pii_fields
from .report import generate_report, save_report, format_summary
from .errors import SchemaGuardError, FileReadError, SchemaError, ValidationError

@click.group(name='schemaguard')
@click.version_option(version=__version__)
def cli():
    """SchemaGuard - Data quality inspection and privacy redaction CLI tool."""
    pass

@cli.command()
@click.argument('filepath', type=click.Path(exists=True, path_type=Path))
def inspect(filepath: Path):
    """Inspect a file and show summary."""
    try:
        headers, rows = read_file(filepath)
        click.echo(f"File: {filepath}")
        click.echo(f"Row count: {len(rows)}")
        click.echo(f"Columns: {', '.join(headers)}")
    except FileReadError as e:
        click.echo(str(e), err=True)
        raise click.Abort()

@cli.command(name='validate')
@click.argument('filepath', type=click.Path(exists=True, path_type=Path))
@click.option('--schema', 'schema_path', type=click.Path(exists=True, path_type=Path), required=True)
@click.pass_context
def validate_cmd(ctx, filepath: Path, schema_path: Path):
    """Validate a file against a schema."""
    try:
        headers, rows = read_file(filepath)
    except FileReadError as e:
        click.echo(f"File Error: {e}", err=True)
        ctx.exit(2)
        
    try:
        schema = load_schema(schema_path)
    except SchemaError as e:
        click.echo(f"Schema Error: {e}", err=True)
        ctx.exit(3)
        
    result = validate(headers, rows, schema)
    
    has_missing_fields = len(result.get("field_errors", [])) > 0
    if has_missing_fields:
        click.echo("Validation Error: Missing required fields found.")
        ctx.exit(1)
        
    has_other_errors = len(result.get("type_errors", [])) > 0
    if has_other_errors:
        click.echo("Validation Error: Type mismatch found.", err=True)
        ctx.exit(1)
        
    if not has_missing_fields and not has_other_errors:
        click.echo("Validation passed.")
        ctx.exit(0)

@cli.command()
@click.argument('filepath', type=click.Path(exists=True, path_type=Path))
@click.option('--output', 'out_path', type=click.Path(path_type=Path), required=False)
@click.option('--fields', '-f', multiple=True, help="Fields to redact")
def redact(filepath: Path, out_path: Path, fields: list[str]):
    """Redact specified fields."""
    try:
        headers, rows = read_file(filepath)
        if not fields:
            fields = detect_pii_fields(headers)
        
        redacted = redact_rows(rows, list(fields))
        
        if out_path is None:
            out_path = filepath.with_name(f"{filepath.stem}_redacted{filepath.suffix}")
        
        if filepath.suffix.lower() == '.csv':
            if len(redacted) > 0:
                out_headers = list(redacted[0].keys())
            else:
                out_headers = headers
            with open(out_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=out_headers)
                writer.writeheader()
                writer.writerows(redacted)
        else:
            with open(out_path, 'w', encoding='utf-8') as f:
                json.dump(redacted, f, indent=2)
                
        click.echo(f"Redacted file saved to {out_path}")
    except Exception as e:
        click.echo(str(e), err=True)
        raise click.Abort()

@cli.command()
@click.argument('filepath', type=click.Path(exists=True, path_type=Path))
@click.option('--schema', 'schema_path', type=click.Path(exists=True, path_type=Path), required=False)
@click.option('--output', 'out_path', type=click.Path(path_type=Path), required=False)
def report(filepath: Path, schema_path: Path, out_path: Path):
    """Generate a JSON report."""
    try:
        headers, rows = read_file(filepath)
        schema = None
        val_result = None
        if schema_path:
            schema = load_schema(schema_path)
            val_result = validate(headers, rows, schema)
            
        rep = generate_report(filepath, headers, rows, schema, val_result)
        if out_path is None:
            out_path = Path("report.json")
        save_report(rep, out_path)
        click.echo(f"Report saved to {out_path}")
        click.echo(format_summary(rep))
    except Exception as e:
        click.echo(str(e), err=True)
        raise click.Abort()

@cli.command()
@click.argument('file1', type=click.Path(exists=True, path_type=Path))
@click.argument('file2', type=click.Path(exists=True, path_type=Path))
def compare(file1: Path, file2: Path):
    """Compare two files."""
    try:
        h1, r1 = read_file(file1)
        h2, r2 = read_file(file2)
        
        click.echo(f"File 1: {len(r1)} rows, {len(h1)} columns")
        click.echo(f"File 2: {len(r2)} rows, {len(h2)} columns")
        
        diff_h = set(h1) ^ set(h2)
        if diff_h:
            click.echo(f"Different columns: {diff_h}")
        else:
            click.echo("Columns are identical.")
    except Exception as e:
        click.echo(str(e), err=True)
        raise click.Abort()

if __name__ == '__main__':
    cli()
