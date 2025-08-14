import click

from pancanki.deck import create_deck
from pancanki.contrib.note_types import FrontBack

@click.group()
def main():
    """A CLI for pancanki."""
    pass

@main.command()
@click.option('--deck-name', required=True, help='The name of the deck to create.')
@click.option('--from-csv', required=True, help='The path to the CSV file.')
@click.option('--note-type', default='FrontBack', help='The note type to use.')
def create_deck_cli(deck_name, from_csv, note_type):
    """Create a new Anki deck from a CSV file."""
    if note_type == 'FrontBack':
        nt = FrontBack()
    else:
        raise click.UsageError(f"Unknown note type: {note_type}")

    deck = create_deck(deck_name=deck_name, from_csv=from_csv, note_types=[nt])
    deck.package()
    click.echo(f"Deck '{deck_name}' created successfully.")

if __name__ == '__main__':
    main()
