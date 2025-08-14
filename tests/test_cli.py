import pytest
from click.testing import CliRunner
from pancanki.cli import main
import pathlib

def test_create_deck_cli():
    runner = CliRunner()
    with runner.isolated_filesystem():
        csv_path = "data.csv"
        with open(csv_path, "w") as f:
            f.write("Question,Answer\n")
            f.write("q1,a1\n")
            f.write("q2,a2\n")

        deck_name = "my-deck"
        result = runner.invoke(main, ['create-deck-cli', '--deck-name', deck_name, '--from-csv', csv_path])

        assert result.exit_code == 0
        assert f"Deck '{deck_name}' created successfully." in result.output

        apkg_path = pathlib.Path(deck_name + ".apkg")
        assert apkg_path.is_file()

def test_create_deck_cli_unknown_note_type():
    runner = CliRunner()
    with runner.isolated_filesystem():
        csv_path = "data.csv"
        with open(csv_path, "w") as f:
            f.write("Question,Answer\n")
            f.write("q1,a1\n")
            f.write("q2,a2\n")

        deck_name = "my-deck"
        result = runner.invoke(main, ['create-deck-cli', '--deck-name', deck_name, '--from-csv', csv_path, '--note-type', 'Unknown'])

        assert result.exit_code != 0
