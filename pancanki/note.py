class Note:
    def __init__(self, note_type, **fields):
        self.note_type = note_type
        self.fields = fields

    def is_valid(self) -> bool:
        pass

    def build_cards(self):
        pass

    def save(self, session) -> None:
        pass
