import io
import warnings
import pathlib
from typing import List, Dict, Tuple

import zipfile
import sqlite3
import tempfile

from . import exceptions


class Deck:
	default_config = {
		'filename': None,
		'extract_to': None,
		'in_memory': False,
		'read_only': False,
		'from_csv': None,
	}

	conn = None
	connection_uri = None
	connection_flags = None
	collection_path = None
	media_path = None

	apkg_file = None
	apkg_filepath = None


	def __init__(self, config=None):
		if self._valid_config(config):
			self.config = config
		else:
			raise exceptions.ConfigurationError('Config is not valid.')

		if self.config is None:
			self.config = self.default_config

		if self.config.get('read_only'):
			self.connection_flags = 'mode=ro'

	def __iter__(self):
		""" Iterate through cards in collection.
		"""
		pass

	def _valid_config(self, config: Dict) -> bool:
		""" Validates a given configuration dictionary.

			For example, `from_csv` cannot be set if `extract_to` is also set.
		"""
		return True

	def _create_connection_in_memory(self) -> None:
		""" Copies collection database 	
		"""
		with open(self.apkg_filepath, 'rb') as fo:
			x_files = zipfile.ZipFile(io.BytesIO(fo.read()))

			temp = tempfile.NamedTemporaryFile(mode='wb')

			with x_files.open('collection.anki2') as db:
				temp.write(db.read())

			temp.close()

			temp_connection = sqlite3.connect(temp.name)

			self.conn = sqlite3.connect(':memory:?' + self.connection_flags, uri=True)

			temp_connection.backup(self.conn)
			temp_connection.close()

	def _create_connection(self) -> None:
		self.conn = sqlite3.connect(self.connecion_uri + '?' + self.connection_flags, uri=True)

	def _close_connection(self) -> None:
		if self.conn:
			self.conn.close()

	def _save_changes(self) -> None:
		pass

	def _open_media(self) -> bool:
		pass

	def cards(self, **filters) -> List[schemas.Card]:
		pass

	def add_card(self, card: schemas.Card):
		pass

	def add_cards(self, cards: List[schemas.Card]):
		pass

	def delete_cards(self, **filters) -> None:
		pass


def new_deck(name: str, from_csv: str = None) -> Deck:
	""" Creates and initializes a new Anki2 deck.
	"""
	cfg = {
		'filename': name,
		'from_csv': from_csv
	}

	d = Deck(cfg)

	return d


def open_deck(filename: str = None, extract_to: str = None, in_memory: bool = False, read_only: bool = False) -> Deck:
	""" Opens an existing Anki2 .apkg file. 
	"""
	if '.apkg' not in filename:
		raise ValueError('Given filename is not valid.')

	cfg = {
		'filename': name,
		'extract_to': extract_to,
		'in_memory': in_memory,
		'read_only': read_only
	}

	d = Deck(cfg)

	return d
