import json
import copy
from typing import List, Dict, NamedTuple

import pystache

from .template import Template
from .field import Field


class NoteType:
    id: str = ''
    deck_id: str = ''
    name: str = ''
    fields: List = []
    templates: List = []
    latex_pre: str = ''
    latex_post: str = ''
    mod: int = 0
    req: List = []
    sortf: int = 0
    tags: List = []
    type: int = 0
    usn: int = 0 
    vers: List = []

    note_type_map = {
        'standard': 0,
        'cloze': 1
    }

    def __init__(self, note_type_id: str = None, deck_id: str = None, fields: List = None, templates: List = None, style: str = None, create_from: Dict = None, **extras):
        if create_from:
            self.load(create_from)

        else:
            self.note_type_id = note_type_id
            self.deck_id = deck_id      
            self.templates = templates
            self.style = style

            if self._valid_fields(fields):
                self.fields = fields

            for i, template in enumerate(self.templates):
                template.ordinal = i

            for i, field in enumerate(self.fields):
                field.ordinal = i

    def __str__(self):
        return self.json

    def load(self, note_type: Dict) -> None:
        """ Creates a note type from an existing JSON string.
        """
        self.note_type_id = list(note_type)[0]
        nt = note_type[self.note_type_id]

        self.deck_id = nt['did']
        self.id = nt['id']
        self.latex_pre = nt['latexPre']
        self.latex_post = nt['latexPost']
        self.mod = nt['mod']
        self.req = nt['req']
        self.sortf = nt['sortf']
        self.tags = nt['tags']
        self.type = nt['type']
        self.usn = nt['usn']
        self.vers = nt['vers']
        self.style = nt['css']
        
        self.templates = [Template(create_from=tmpl) for tmpl in nt['tmpls']]
        self.fields = [Field(create_from=fld) for fld in nt['flds']]

    def _prepare_req(self) -> List:
        """ Generates the required fields of the JSON string.

        This method is taken from kerrickstanley et al. over at genanki since I couldn't think of
        a better solution to implement myself :)

        See: https://github.com/kerrickstaley/genanki/blob/master/genanki/model.py#L32
        """
        req = []

        field_names = [field.name for field in self.fields]
        garbage_value = '_1GarabGE_'

        for template in self.templates:
            field_values = {field: garbage_value for field in field_names}
            required_fields = []

            for field_ordinal, field in enumerate(field_names):
                fv_copy = copy.copy(field_values)
                fv_copy[field] = ''

                rendered = pystache.render(template.question_format, fv_copy)

                if garbage_value not in rendered:
                    required_fields.append(field_ordinal)

            if required_fields:
                req.append([template.ordinal, 'all', required_fields])
                continue

        for template in self.templates:
            field_values = {field: garbage_value for field in field_names}
            required_fields = []

            for field_ordinal, field in enumerate(field_names):
                fv_copy = copy.copy(field_values)
                fv_copy[field] = garbage_value

                rendered = pystache.render(template.question_format, fv_copy)

                if garbage_value in rendered:
                    required_fields.append(field_ordinal)

            if required_fields:
                req.append([template.ordinal, 'any', required_fields])
        
        return req

    def prepare(self) -> Dict:
        """ Constructs a dictionary that is used to populate the deck's `models` column in its `col` table.
        """
        note_type = {
            self.note_type_id: {
                'css': self.style if self.style else '',
                'did': self.deck_id,
                'flds': [ {
                    'font': fld.font_family,
                    'media': fld.media,
                    'name': fld.name,
                    'ord': fld.ordinal,
                    'rtl': fld.right_to_left_script,
                    'size': fld.font_size,
                    'sticky': fld.sticky
                    } for fld in self.fields ],
                'id': self.note_type_id,
                'latexPre': self.latex_pre,
                'latexPost': self.latex_post,
                'mod': 0,
                'name': self.name,
                'req': self._prepare_req(),
                'sortf': 0,
                'tags': [],
                'tmpls': [ {
                    'afmt': tmpl.answer_format,
                    'bafmt': tmpl.browser_answer_format,
                    'bqfmt': tmpl.browser_question_format,
                    'did': tmpl.deck_id,
                    'name': tmpl.name,
                    'ord': tmpl.ordinal,
                    'qfmt': tmpl.question_format
                    } for tmpl in self.templates ],
                'type': self.type,
                'usn': self.usn,
                'vers': self.vers
            }
        }
    
        return note_type

    @property
    def json(self) -> str:
        """ Returns JSON string.
        """
        return json.dumps(self.prepare())

