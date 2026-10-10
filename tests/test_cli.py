from click.testing import CliRunner
from schemaguard.cli import cli

def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "version" in result.output.lower()

def test_inspect_csv(tmp_csv):
    runner = CliRunner()
    result = runner.invoke(cli, ["inspect", str(tmp_csv)])
    assert result.exit_code == 0

def test_inspect_json(tmp_json):
    runner = CliRunner()
    result = runner.invoke(cli, ["inspect", str(tmp_json)])
    assert result.exit_code == 0

def test_validate_valid(tmp_csv, sample_schema):
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", str(tmp_csv), "--schema", sample_schema])
    assert result.exit_code == 0

def test_validate_invalid(tmp_csv_empty, sample_schema):
    runner = CliRunner()
    result = runner.invoke(cli, ["validate", str(tmp_csv_empty), "--schema", sample_schema])
    assert result.exit_code != 0

def test_redact_basic(tmp_csv, tmp_path):
    runner = CliRunner()
    out = tmp_path / "out.csv"
    result = runner.invoke(cli, ["redact", str(tmp_csv), "--output", str(out), "--fields", "email"])
    assert result.exit_code == 0
    assert out.exists()

def test_report_basic(tmp_csv, sample_schema, tmp_path):
    runner = CliRunner()
    out = tmp_path / "report.json"
    result = runner.invoke(cli, ["report", str(tmp_csv), "--schema", sample_schema, "--output", str(out)])
    assert result.exit_code == 0
    assert out.exists()

def test_file_not_found():
    runner = CliRunner()
    result = runner.invoke(cli, ["inspect", "nonexistent.csv"])
    assert result.exit_code == 2
