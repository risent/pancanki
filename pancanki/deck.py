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

    note_types = []

    def __init__(self, filename, action: str = None, **options):
        self.action = action
        self.options = options
        self.apkg_file = pathlib.Path(filename)

        if self.action == 'open':
            self._create_connection_to_existing_collection(extract_to=options.get('extract_to', ''))
            
        elif action == 'create':
            self.apkg_dir = self.apkg_file
            self._create_connection_and_collection()

        else:
            raise 'Invalid action.'

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
        database.Base.metadata.create_all(config.Engine)

        self.collection = Session(config.Engine)
        self._get_note_types()

    def _create_connection_and_collection(self) -> None:
        self.apkg_dir.mkdir()

        collection_path = self.apkg_dir / 'collection.anki2'
        collection_path.touch()

        config.Engine = create_engine('sqlite:///' + str(collection_path.absolute()))
        database.Base.metadata.create_all(config.Engine)

        self.collection = Session(config.Engine)

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
            note_type = self.note_types[0]

        new_note = None

    def delete_note(self, note_id) -> None:
        pass

    def _close(self) -> None:
        if self.colleciton:
            self.colleciton.close()

    def save(self, *args, **kwargs) -> None:
        if self.collection:
            self.collection.commit(*args, **kwargs)

    def package(self, filename: str = None) -> None:
        pass

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

    d = Deck(deck_name, action='create', from_csv=from_csv)

    return d