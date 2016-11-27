from newmansound.model import Album, Artist, Song
from tests.fixtures import engine, session


def add_album(session, name=''):
    return _add(session, Album, name)


def add_artist(session, name=''):
    return _add(session, Artist, name)


def add_song(session, path='', name=''):
    song = Song()
    song.name = name
    song.path = path
    session.add(song)
    session.commit()

    return song


def _add(session, type, name):
    object  = type()
    object.name = name
    session.add(object)
    session.commit()

    return object
