import time
import json
import random
import pathlib
from typing import List, Dict, Tuple

import zipfile
import sqlite3
import tempfile

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session

from . import config, database
from .note_type import NoteType


class Deck:
    deck_id = None
    collection_path = None
    connection_flags = ''
    media_path = None

    collection = None

    apkg_dir = None
    apkg_file = None
    apkg_filepath = None

    note_types = []

    def __init__(self, filename: str = None, action: str = None, **options):
        self.apkg_file = pathlib.Path(filename)
        self.action = action
        self.options = options

        if self.action == 'open':
            self._create_connection_to_existing_collection(extract_to=options.get('extract_to', ''))
            
        elif action == 'create':
            self._create_connection_and_collection()

        else:
            raise 'Invalid action.'

    def __iter__(self):
        """ Iterate through cards in collection.
        """
        pass

    def _generate_deck_id(self) -> int:
        """ Sets the deck's deck_id attribute to a random 32-bit integer and returns it.
        """
        self.deck_id = random.getrandombits(32)

        return self.deck_id

    def _create_connection_to_existing_collection(self, extract_to: str = '') -> None:
        """ Sets connection as a standard connection based on unzipped .apkg file.
        """
        z = zipfile.ZipFile(self.apkg_file)

        self.apkg_dir = pathlib.Path(extract_to) / str('.temp_' + str(int(time.time())))
        collection_path = self.apkg_dir / 'collection.anki2'
        
        z.extractall(path=self.apkg_dir)

        config.Engine = create_engine('sqlite:///' + str(collection_path.absolute()))        
        self.collection = Session(config.Engine)
        config.Base.prepare(config.Engine, reflect=True)

        self._get_note_types()

    def _get_note_types(self) -> None:
        note_types = json.loads(self.collection.query(database.Collection).first().models)

        for nt_id in note_types:
            note = {nt_id: note_types[nt_id]}

            self.note_types.append(NoteType(create_from=note))

    def notes(self) -> List:
        return self.collection.query(database.Note).all()

    def cards(self) -> List:
        return self.collection.query(database.Card).all()

    def add_note(self, **fields) -> None:
        pass

    def delete_note(self, note_id: str = None, **fields) -> None:
        pass

    def save(self, *args, **kwargs) -> None:
        if self.collection:
            self.collection.commit(*args, **kwargs)

    def close(self) -> None:
        if self.colleciton:
            self.colleciton.close()

    @property
    def size(self):
        """ Returns the number of cards in the deck.
        """

        return self.collection.query(database.Card).count()


def open_deck(apkg_file: str, read_only=True) -> Deck:
    """ Opens an existing Anki2 .apkg file. 
    """

    d = Deck(filename=apkg_file, action='open', read_only=True)

    return d


def create_deck(deck_name: str) -> Deck:
    pass