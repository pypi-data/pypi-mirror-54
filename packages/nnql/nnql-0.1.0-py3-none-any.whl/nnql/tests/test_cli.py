from nnql.cli import nnql

from click.testing import CliRunner


def test_tool():
    runner = CliRunner()
    result = runner.invoke(nnql, ["--tool", "abc"])
    assert result.exit_code == 0
    assert result.output == "abc\n"


def test_t():
    runner = CliRunner()
    result = runner.invoke(nnql, ["-t", "abc"])
    assert result.exit_code == 0
    assert result.output == "abc\n"
