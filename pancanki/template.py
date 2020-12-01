from typing import List


class Template:
    ordinal: str = None     # to be set during NoteType creation

    def __init__(self, name, answer_format: str = None, question_format: str = None, **extras):
        self.answer_format = answer_format
        self.question_format = question_format

        self.extras = extras

        if self.extras.get('ordinal'):
            self.ordinal = self.extras.get('ordinal')
