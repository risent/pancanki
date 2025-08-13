import pytest
from pancanki.deck import create_deck, Deck
import pathlib

def test_create_deck(tmp_path):
    deck_path = tmp_path / "test_deck"
    deck = create_deck(str(deck_path))
    assert isinstance(deck, Deck)
    assert deck_path.is_dir()
