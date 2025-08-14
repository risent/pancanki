import pytest
from pancanki.note_type import NoteType

def test_create_note_type_from_dict():
    note_type_data = {
        '12345': {
            'id': '12345',
            'name': 'Test Note Type',
            'flds': [
                {'name': 'Front', 'ord': 0, 'font': 'Arial', 'size': 20, 'rtl': False, 'sticky': False, 'media': []},
                {'name': 'Back', 'ord': 1, 'font': 'Arial', 'size': 20, 'rtl': False, 'sticky': False, 'media': []}
            ],
            'tmpls': [{'name': 'Card 1', 'qfmt': '{{Front}}', 'afmt': '{{Back}}', 'ord': 0, 'did': '123', 'bafmt': '', 'bqfmt': ''}],
            'css': '',
            'did': '123',
            'latexPre': '',
            'latexPost': '',
            'mod': 0,
            'req': [],
            'sortf': 0,
            'tags': [],
            'type': 0,
            'usn': 0,
            'vers': []
        }
    }
    note_type = NoteType(create_from=note_type_data)
    assert note_type.id == '12345'
    assert note_type.name == 'Test Note Type'
    assert len(note_type.fields) == 2
    assert len(note_type.templates) == 1
