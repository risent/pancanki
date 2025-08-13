import time
import hashlib

from pancanki import database


def sha1(s):
    return hashlib.sha1(s.encode('utf-8')).hexdigest()

def guid_for(data):
    return sha1(data)


class Note:
    def __init__(self, note_type, fields):
        self.note_type = note_type
        self.fields = fields
        self.guid = guid_for(self.fields[0])

    def is_valid(self) -> bool:
        return len(self.fields) == len(self.note_type.fields)

    def build_cards(self):
        pass

    def save(self, session) -> None:
        if not self.is_valid():
            raise ValueError("The number of fields does not match the note type.")

        flds = '\x1f'.join(self.fields)
        sfld = self.fields[self.note_type.sortf]

        note = database.Note(
            guid=self.guid,
            mid=self.note_type.id,
            mod=int(time.time()),
            usn=0,
            tags='',
            flds=flds,
            sfld=sfld,
            csum=int(sha1(sfld)[:8], 16),
            flags=0,
            data='',
        )

        session.add(note)
        session.commit()
