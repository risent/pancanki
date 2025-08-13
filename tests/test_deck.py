import pytest
from pancanki.deck import create_deck, open_deck, Deck
from pancanki.field import Field
from pancanki.template import Template
from pancanki.note_type import NoteType
import pathlib
import zipfile

def test_create_deck(tmp_path):
    deck_path = tmp_path / "test_deck"
    deck = create_deck(str(deck_path))
    assert isinstance(deck, Deck)
    assert deck_path.is_dir()

def test_add_note_and_package(tmp_path):
    deck_path = tmp_path / "test_deck"
    deck = create_deck(str(deck_path))

    field1 = Field(name='Question')
    field2 = Field(name='Answer')
    template = Template(name='Card 1', question_format='{{Question}}', answer_format='{{Answer}}')
    note_type = NoteType(note_type_id='12345', deck_id=deck.deck_id, name='Simple', fields=[field1, field2], templates=[template])
    deck.add_note_type(note_type)

    deck.add_note(note_type, Question='What is the capital of France?', Answer='Paris')

    assert len(deck.notes) == 1
    assert deck.notes[0].flds == 'What is the capital of France?\x1fParis'

    package_path = tmp_path / "test_deck.apkg"
    deck.package(str(package_path))

    assert package_path.is_file()

    with zipfile.ZipFile(package_path, 'r') as z:
        assert 'collection.anki2' in z.namelist()
        assert 'media' in z.namelist()

def test_open_deck(tmp_path):
    deck_path = tmp_path / "test_deck"
    deck = create_deck(str(deck_path))
    field1 = Field(name='Question')
    field2 = Field(name='Answer')
    template = Template(name='Card 1', question_format='{{Question}}', answer_format='{{Answer}}')
    note_type = NoteType(note_type_id='12345', deck_id=deck.deck_id, name='Simple', fields=[field1, field2], templates=[template])
    deck.add_note_type(note_type)
    deck.add_note(note_type, Question='What is the capital of France?', Answer='Paris')
    package_path = tmp_path / "test_deck.apkg"
    deck.package(str(package_path))

    opened_deck = open_deck(str(package_path))

    assert len(opened_deck.notes) == 1
    assert opened_deck.notes[0].flds == 'What is the capital of France?\x1fParis'

def test_create_deck_with_custom_note_type(tmp_path):
    deck_path = tmp_path / "test_deck"

    templates = [
        Template('Card 1', question_format='{{Question}}', answer_format='{{Answer}}')
    ]
    fields = [
        Field('Question'),
        Field('Answer')
    ]
    note_type = NoteType(note_type_id='54321', deck_id='123', name='Custom', fields=fields, templates=templates)

    deck = create_deck(str(deck_path), note_types=[note_type])

    deck.add_note(note_type, Question='q1', Answer='a1')

    assert len(deck.notes) == 1
    assert deck.notes[0].flds == 'q1\x1fa1'
