from pancanki.note_type import NoteType
from pancanki.field import Field
from pancanki.template import Template


class FrontBack(NoteType):
    def __init__(self, **kwargs):
        fields = [
            Field(name='Front'),
            Field(name='Back'),
        ]
        templates = [
            Template(
                name='Card 1',
                question_format='{{Front}}',
                answer_format='{{FrontSide}}<hr id="answer">{{Back}}',
            ),
        ]
        super().__init__(note_type_id='123456789', fields=fields, templates=templates, **kwargs)