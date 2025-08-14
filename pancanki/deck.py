import time
import json
import random
import pathlib
from typing import List, Dict, Tuple

import zipfile
import sqlite3
import tempfile

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base

from pancanki import config, database
from pancanki.note import Note
from pancanki.note_type import NoteType


class Deck:
    deck_id = None
    collection_path = None
    connection_flags = ''
    media_path = None

    collection = None

    apkg_dir = None
    apkg_file = None
    apkg_filepath = None

    def __init__(self, filename, action: str = None, **options):
        self.note_types = []
        self.action = action
        self.options = options
        self.apkg_file = pathlib.Path(filename)
        self.name = self.apkg_file.stem
        self.engine = None

        if self.action == 'open':
            self._create_connection_to_existing_collection(extract_to=options.get('extract_to', ''))
            
        elif action == 'create':
            self.apkg_dir = self.apkg_file
            self._generate_deck_id()
            self._create_connection_and_collection()

            if options.get('note_types'):
                self.note_types = options.get('note_types')

            col = database.Collection(
                id=1,
                crt=int(time.time()),
                mod=int(time.time()),
                scm=int(time.time()),
                ver=11,
                dty=0,
                usn=0,
                ls=0,
                conf='{"nextPos": 1, "estTimes": true, "activeDecks": [1], "sortType": "noteFld", "timeLim": 0, "sortBackwards": false, "addToCur": true, "curDeck": 1, "newBury": true, "newSpread": 0, "dueCounts": true, "curModel": "1564944648016", "collapseTime": 1200}',
                models=self._prepare_models_json(),
                decks=self._prepare_decks_json(),
                dconf='{"1": {"name": "Default", "replayq": true, "lapse": {"leechFails": 8, "minInt": 1, "delays": [10], "leechAction": 0, "mult": 0}, "rev": {"perDay": 200, "ivlFct": 1, "maxIvl": 36500, "minSpace": 1, "ease4": 1.3, "bury": true, "hardFactor": 1.2}, "timer": 0, "maxTaken": 60, "new": {"perDay": 20, "delays": [1, 10], "separate": true, "ints": [1, 4, 7], "initialFactor": 2500, "bury": true, "order": 1}, "mod": 0, "usn": 0}}',
                tags='{}'
            )
            self.collection.add(col)
            self.collection.commit()

        else:
            raise Exception('Invalid action.')

    def _generate_deck_id(self) -> int:
        """ Sets the deck's deck_id attribute to a random 32-bit integer and returns it.
        """
        self.deck_id = random.getrandbits(32)

        return self.deck_id

    def _create_connection_to_existing_collection(self, extract_to: str = '') -> None:
        """ Sets connection as a standard connection based on unzipped .apkg file.
        """
        z = zipfile.ZipFile(self.apkg_file)

        self.apkg_dir = pathlib.Path(extract_to) / str('.temp_' + str(int(time.time())))
        collection_path = self.apkg_dir / 'collection.anki2'
        
        z.extractall(path=self.apkg_dir)

        self.engine = create_engine('sqlite:///' + str(collection_path.absolute()))
        self.collection = Session(self.engine)

        self._get_note_types()

    def _create_connection_and_collection(self) -> None:
        self.apkg_dir.mkdir()

        collection_path = self.apkg_dir / 'collection.anki2'
        collection_path.touch()

        self.engine = create_engine('sqlite:///' + str(collection_path.absolute()))
        database.Base.metadata.create_all(self.engine, checkfirst=True)

        self.collection = Session(self.engine)

    def _get_note_types(self) -> None:
        note_types = json.loads(self.collection.query(database.Collection).first().models)

        for nt_id in note_types:
            note = {nt_id: note_types[nt_id]}

            self.note_types.append(NoteType(create_from=note))

    def create_node_type(self, templates: List, fields: List, style: str = None, **extras) -> NoteType:
        """ Creates a new note type and adds it to the deck.
        """

        note_type = NoteType(deck_id=self.deck_id, templates=templates, fields=fields, style=style, **extras)

        self.note_types.append(note_type)
        self.save()

    def add_note_type(self, note_type) -> None:
        """ Adds a new note type to the deck.
        """

        self.note_types.append(note_type)

        col = self.collection.query(database.Collection).first()
        self.save()

    def add_note(self, note_type, **fields) -> None:
        if note_type is None:
            if not self.note_types:
                raise ValueError("Deck has no note types.")
            note_type = self.note_types[0]

        field_values = [fields[field.name] for field in note_type.fields]
        new_note = Note(note_type=note_type, fields=field_values)
        new_note.save(self.collection)

    def delete_note(self, note_id) -> None:
        note = self.collection.query(database.Note).filter_by(id=note_id).first()
        if note:
            for card in note.cards:
                self.collection.delete(card)
            self.collection.delete(note)
            self.collection.commit()

    def _close(self) -> None:
        if self.collection:
            self.collection.close()

    def save(self, *args, **kwargs) -> None:
        if self.collection:
            self.collection.commit(*args, **kwargs)

    def _prepare_decks_json(self):
        decks = {
            "1": {
                "id": 1,
                "name": "Default",
                "mod": int(time.time()),
                "usn": -1,
                "desc": "",
                "dyn": 0,
                "conf": 1,
                "extendNew": 10,
                "extendRev": 50,
                "collapsed": True
            },
            str(self.deck_id): {
                "id": self.deck_id,
                "name": self.name,
                "mod": int(time.time()),
                "usn": -1,
                "desc": "",
                "dyn": 0,
                "conf": 1,
                "extendNew": 10,
                "extendRev": 50,
                "collapsed": False,
            }
        }
        return json.dumps(decks)

    def _prepare_models_json(self):
        models = {}
        for nt in self.note_types:
            models.update(nt.prepare())
        return json.dumps(models)

    def package(self, filename: str = None) -> None:
        if filename is None:
            filename = self.name + ".apkg"

        col = self.collection.query(database.Collection).first()
        col.models = self._prepare_models_json()
        col.decks = self._prepare_decks_json()
        self.collection.commit()

        db_path = self.apkg_dir / 'collection.anki2'

        with zipfile.ZipFile(filename, 'w') as z:
            z.write(db_path, 'collection.anki2')

            media_files = {}
            if self.media_path and pathlib.Path(self.media_path).is_dir():
                for i, media_file in enumerate(pathlib.Path(self.media_path).iterdir()):
                    z.write(media_file, str(i))
                    media_files[str(i)] = media_file.name

            z.writestr('media', json.dumps(media_files))

    @property
    def notes(self) -> List:
        """ Returns a list of all notes in the deck.
        """

        return self.collection.query(database.Note).all()

    @property
    def cards(self) -> List:
        """ Returns a list of all cards in the deck.
        """

        return self.collection.query(database.Card).all()

    @property
    def size(self):
        """ Returns the number of cards in the deck.
        """

        return self.collection.query(database.Card).count()


def open_deck(apkg_file: str) -> Deck:
    """ Opens an existing Anki2 .apkg file. 
    """

    d = Deck(apkg_file, action='open')

    return d


def create_deck(deck_name: str, from_csv: str = None, note_types: List = None) -> Deck:
    """ Initializes an Anki2 deck.
    """

    d = Deck(deck_name, action='create', from_csv=from_csv, note_types=note_types)

    return d