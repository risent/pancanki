# pancanki
A fast and easy to use library for creating, editing, and reading Anki decks.

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
```

### Creating a New Deck

```python
from pancanki import create_deck

deck = create_deck('my_new_deck')


```

### Create a New Deck from a CSV File

```python
from pancanki import create_deck

deck = create_deck('my_new_deck', from_csv='path/to/my_data.csv')

print(deck.cards)
# [<Card: 0>, <Card: 1>, ...]
```

## Documentation

While `pancanki` gives you the open to create a Deck instance from scratch, it's highly recommended you use one of the two high-level
function `open_deck` or `create_deck`.

#### open_deck

`def open_deck(filename: str = None, extract_to: str = None, in_memory: bool = False, read_only: bool = False) -> Deck`

A high level function used for opening an existing Anki deck. This function only accepts compressed files with the extension `.apkg` and
nothing else. 

Parameters

`filename: str` The compressed Anki deck file (the .apkg file) that you wish to open.

`extract_to: str` Optional path and directory you wish you extract the .apkg file to. Leaving as `None` will delete the uncompressed 
files once you close the deck. Note that once you close a deck, all the files are compressed back into a valid .apkg file.

`in_memory: bool` If set to `True`, `pancanki` will attempt to uncompress the .apkg file and load all the resources into memory 
(including the database). If you want fast *really* reads, it's recommemded you use this mode in combination with `read_only`.
Note that a lot of Anki decks are *very* large and probably won't fit into memory.

`read_only: bool` If set to `True`, `pancanki` will open all files and the database connection in read only mode. Adding, editing, 
or deleting of cards as well as any other edits you'd like to make to the deck are disabled if set to `True`.

#### create_deck



#### Deck

`pancanki` manages Anki decks using a single `Deck` object. 