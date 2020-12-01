import json
from typing import List, Dict


class Template:
    ordinal: int = 0
    name: str = ''
    deck_id: str = ''
    answer_format: str = ''
    question_format: str = ''
    browser_answer_format: str = ''
    browser_question_format: str = ''

    def __init__(self, name: str = None, answer_format: str = None, question_format: str = None, create_from: Dict = None, **extras):
        if create_from:
            self.load(create_from)

        else:
            if name is None:
                raise 'Name must not be None.'

            if answer_format is None:
                raise 'answer_format...'

            self.name = name
            self.answer_format = answer_format
            self.question_format = question_format

            self.extras = extras

            self.ordinal = self.extras.get('ordinal', 0)
            self.deck_id = self.extras.get('deck_id', '')
            self.browser_answer_format = self.extras.get('browser_answer_format', '')
            self.browser_question_format = self.extras.get('browser_question_format', '')

    def __str__(self):
        return self.json

    def load(self, template: Dict) -> None:
        self.ordinal = template['ord']
        self.deck_id = template['did']
        self.name = template['name']
        self.answer_format = template['afmt']
        self.question_format = template['qfmt']
        self.browser_answer_format = template['bafmt']
        self.browser_question_format = template['bqfmt']

    def prepare(self) -> Dict:
        template = {
            'afmt': self.answer_format,
            'bafmt': self.browser_answer_format,
            'bqfmt': self.browser_question_format,
            'did': self.deck_id,
            'name': self.name,
            'ord': self.ordinal,
            'qfmt': self.question_format
        }

        return template

    @property
    def json(self) -> str:
        return json.dumps(self.prepare())
    