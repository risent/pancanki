# pancanki
A fast and easy to use library for creating and reading Anki decks.

## Installing

```
pip install pancanki
```

## Quickstart

#### Opening an Existing Deck

```python
from pancanki import open_deck

deck = open_deck('path/to/my_anki_deck.apkg')

print(deck.size)
# 42

my_note_type = deck.note_types[0]

print(my_note_type.style)
# .card { ... }

my_note_type.style = '.card {font-family: arial; font-size: 20px; text-align: center; color: black; background-color: white;}'

deck.package()
```

### Creating a New Deck

```python
import pancanki

template = pancanki.Template('Card 1', question_format='{{Question}}<br>{{Picture}}', answer_format='{{FrontSide}}<hr id="answer">{{Answer}}')
fields = [pancanki.Field('Question'), pancanki.Field('Picture', media_type='img'), pancanki.Field('Answer')]
note_type = pancanki.NoteType(templates=[template], fields=fields)

deck = pancanki.create_deck('My Deck', media_dir='my_media/', note_type=note_type)

deck.add_note(question='How do you exit vi without saving changes?', picture='vi.jpeg', answer=':qa!')

deck.package()
```

### Create a New Deck from a CSV File

```python
from pancanki import create_deck

template = pancanki.Template('Card 1', question_format='{{ColumnA}}', answer_format='{{FrontSide}}<hr id="answer">{{ColumnB}}')
fields = [pancanki.Field('ColumnA'), pancanki.Field('ColumnB')]
my_note_type = pancanki.NoteType(templates=[template], fields=fields)

deck = create_deck('My Deck', from_csv='path/to/my_data.csv', note_type=my_note_type)

deck.package()
```

## Documentation

While `pancanki` gives you the option to create a Deck instance from scratch, it's highly recommended you use one of the two high-level
functions `open_deck` or `create_deck`.


#### create_deck

`def create_deck(deck_name: str, note_type: NoteType = None, from_csv: str = None, media_dir: str = None) -> Deck`

A high-level function used for creating a new Anki deck.

*Parameters*

`deck_name: str` The name of the deck you want to create. If you do not specify, when you package your deck, it will be saved as `deck_name.apkg`.

`note_type: NoteType` A valid NoteType instance. If you do not specify one, the deck will default to a standard note type.

`from_csv: str` A path to CSV file. Each row will create a note in the deck when you call `deck.package()`. *If you're specifying a custom note type
it's important that you ensure that the number of fields is equal to the number of columns of your CSV file. See the above example.*

`media_dir: str` A path to a directory that contains all the deck's media files needed to add notes. All files under this directory will be included in
your package when calling `deck.package()`. Leaving as `None` will not set any directory and it's assumed the deck has no media.


#### open_deck

`def open_deck(filename, extract_to: str = None) -> Deck`

A high level function used for opening an existing Anki deck. This function only accepts compressed files with the extension `.apkg` and
nothing else. 

*Parameters*

`filename: str` The compressed Anki deck file (the .apkg file) that you wish to open.

`extract_to: str` Optional path and directory you wish you extract the .apkg file to. Leaving as `None` will delete the uncompressed 
files once you close the deck. Note that once you close a deck, all the files are compressed back into a valid .apkg file.


#### The Deck Object

`pancanki` manages Anki decks using a single `Deck` object. A `Deck` is returned when you call `open_deck` or `create_deck`.

*Useful Attributes & Properties*

`deck_id: int` a 32-bit integer used to idenify the deck within Anki. Read more about deck ids here.

`collection: sqlalchemy.Session` The database session used to interaction with the collection.anki2 SQLite3 database.

`note_type: NoteType` The note type that the deck uses.

`size: int` Returns the number of cards in the deck.

*Useful Methods*

`notes() -> List` Returns all the notes within the deck as a list.

`cards() -> List` Returns all the cards within the deck as a list.

`add_note(**fields) -> None` Creates a new note.

`delete_note(**fields) -> None` Removes the first note in the deck that matches the given fields. If a note is deleted, all cards under that note are also deleted from the deck.

`save() -> None` Saves and commits all changes to the collection database. Read more about saving.

`close(save: bool=True) -> None` Optionally saves and closes the connection to the database and 

#### Card Types

## Credits

Inspired by [genanki](https://github.com/kerrickstaley/genanki)