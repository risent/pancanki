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

some_cards = deck.cards(type='new')
# [<Card: ...>, <Card: ...>, ...]

# Iterate through all cards in the deck and make edits to them.
for card in deck:
	card.style = None

# Commits changes to cards and save any other changes made to the deck.
deck.save()

# Recompresses files and removes all uncompressed files. Cleans up.
deck.close()
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

`def create_deck(deck_name: str, note_type: NoteType = None, from_csv: str = None, media: str = None) -> Deck`

A high-level function used for creating a new Anki deck.

__Parameters__

`deck_name: str` The name of the deck you want to create. If you do not specify, when you package your deck, it will be saved as `deck_name.apkg`.

`note_type: NoteType` A valid NoteType instance. If you do not specify one, the deck will default to a standard note type.

`from_csv: str` A path to CSV file. Each row will create a note in the deck when you call `deck.package()`. *If you're specifying a custom note type
it's important that you ensure that the number of fields is equal to the number of columns of your CSV file. See the above example.*

`media_dir: str` A path to a directory that contains all the deck's media files needed to add notes. All files under this directory will be included in
your package when calling `deck.package()`. Leaving as `None` will not set any directory and it's assumed the deck has no media.


#### open_deck

`def open_deck(filename, extract_to: str = None, in_memory: bool = False, read_only: bool = False) -> Deck`

A high level function used for opening an existing Anki deck. This function only accepts compressed files with the extension `.apkg` and
nothing else. 

__Parameters__

`filename: str` The compressed Anki deck file (the .apkg file) that you wish to open.

`extract_to: str` Optional path and directory you wish you extract the .apkg file to. Leaving as `None` will delete the uncompressed 
files once you close the deck. Note that once you close a deck, all the files are compressed back into a valid .apkg file.

`in_memory: bool` If set to `True`, `pancanki` will attempt to uncompress the .apkg file and load all the resources into memory 
(including the database). If you want *really* fast reads, it's recommemded you use this mode in combination with `read_only` mode.
Note that a lot of Anki decks are very large and probably won't fit into memory.

`read_only: bool` If set to `True`, `pancanki` will open all files and the database connection in read only mode. Adding, editing, 
or deleting of cards as well as any other edits you'd like to make to the deck are disabled if set to `True`.

#### create_deck



#### Deck

`pancanki` manages Anki decks using a single `Deck` object. 


## Credits

Inspired by [genanki](https://github.com/kerrickstaley/genanki)