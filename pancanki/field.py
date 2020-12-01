import json
from typing import List, Dict


class Field:
    ordinal: int = 0
    font_family: str = ''
    font_size: str = ''
    media: List = []
    name: str = ''
    right_to_left_script: bool = False
    sticky: str = ''

    def __init__(self, name: str = None, media: List = None, create_from: Dict = None, **extras):
        if create_from:
            self.load(create_from)

        else:
            if name is None:
                raise 'Name must not be None.'

            self.name = name
            self.extras = extras

            self.ordinal = self.extras.get('ordinal', 0)
            self.font_family = self.extras.get('font_family', '')
            self.font_size = self.extras.get('font_size', '')
            self.media = self.extras.get('media', '')
            self.right_to_left_script = self.extras.get('rtl', False)
            self.sticky = self.extras.get('sticky', '')

    def __str__(self):
        return self.json

    def load(self, field: Dict) -> None:
        self.ordinal = field['ord']
        self.name = field['name']
        self.media = field['media']
        self.font_family = field['font']
        self.font_size = field['size']
        self.right_to_left_script = field['rtl']
        self.sticky = field['sticky']

    def prepare(self) -> Dict:
            field = {
                'font': self.font_family,
                'media': self.media,
                'name': self.name,
                'ord': self.ordinal,
                'rtl': self.right_to_left_script,
                'size': self.font_size,
                'sticky': self.sticky
            }

            return field

    @property
    def json(self) -> str:
        return json.dumps(self.prepare()) 