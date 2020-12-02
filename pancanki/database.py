import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Index
from sqlalchemy.orm import relationship

from . import config


Base = declarative_base() 


class Collection(Base):
    __tablename__ = 'col'

    id = Column(Integer, primary_key=True)
    crt = Column(Integer)
    mod = Column(Integer)
    scm = Column(Integer)
    ver = Column(Integer)
    dty = Column(Integer)
    usn = Column(Integer, default=0)
    ls = Column(Integer)
    conf = Column(String)
    models = Column(String)
    decks = Column(String)
    dconf = Column(String)
    tags = Column(String)


class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    guid = Column(String)
    mid = Column(Integer)
    mod = Column(Integer)
    usn = Column(Integer)
    tags = Column(String)
    flds = Column(String)
    sfld = Column(Integer)
    csum = Column(Integer)
    flags = Column(Integer, default=0)
    data = Column(String, default='')

    cards = relationship('Card')


class Card(Base):
    __tablename__ = 'cards'

    id = Column(Integer, primary_key=True)
    nid = Column(Integer, ForeignKey('notes.id'))
    did = Column(Integer)
    ord = Column(Integer)
    mod = Column(Integer)
    usn = Column(Integer, default=0)
    type = Column(Integer, default=0)
    queue = Column(Integer)
    due = Column(Integer)
    ivl = Column(Integer)
    factor = Column(Integer)
    reps = Column(Integer)
    lapses = Column(Integer)
    left = Column(Integer)
    odue = Column(Integer)
    odid = Column(Integer)
    flags = Column(Integer)
    data = Column(String, default='')

    note = relationship('Note')
    revisions = relationship('RevisionLog')

class Grave(Base):
    __tablename__ = 'graves'

    id = Column(Integer, primary_key=True)
    usn = Column(Integer, default=-1)
    oid = Column(Integer)
    type = Column(Integer)


class RevisionLog(Base):
    __tablename__ = 'revlog'

    id = Column(Integer, primary_key=True)
    cid = Column(Integer, ForeignKey('cards.id'))
    usn = Column(Integer, default=0)
    ease = Column(Integer)
    ivl = Column(Integer)
    lastIvl = Column(Integer)
    factor = Column(Integer)
    time = Column(Integer)
    type = Column(Integer)


def create_indexes(engine):
    try:
        Index('ix_cards_nid', Card.nid).create(bind=engine)
        Index('ix_cards_sched', Card.did, Card.queue, Card.due).create(bind=engine)
        Index('ix_cards_usn', Cards.usn).create(bind=engine)
        Index('ix_notes_csum', Note.csum).create(bind=engine)
        Index('ix_notes_usn', Note.usn).create(bind=engine)
        Index('ix_revlog_cid', RevisionLog.cid).create(bind=engine)
        Index('ix_revlog_usn', RevisionLog.usn).create(bind=engine)
    
    except Exception:
        # the indexes are already created
        pass
