import pytest
from pancanki.note import Note
from pancanki.note_type import NoteType
from pancanki.field import Field

def test_save_invalid_note():
    field1 = Field(name='Question')
    field2 = Field(name='Answer')
    note_type = NoteType(note_type_id='123', name='Simple', fields=[field1, field2], templates=[])

    note = Note(note_type=note_type, fields=['q1'])

    with pytest.raises(ValueError):
        note.save(session=None)
