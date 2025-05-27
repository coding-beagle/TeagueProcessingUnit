from TeagueASM.main import cli
from pathlib import Path
from click.testing import CliRunner


def test_file():
    # Get the directory where this test file is located
    test_dir = Path(__file__).parent
    # Construct path to the test .tgasm file
    test_file_path = test_dir / "mvp_test.tgasm"

    # Use Click's CliRunner to test the CLI command
    runner = CliRunner()
    result = runner.invoke(cli, ["asm2hex", str(test_file_path)])

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Command failed with output: {result.output}"
