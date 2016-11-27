from newmansound.model import Song
from tests.fixtures import engine, session


def add_song(session, path='', name=''):
    song = Song()
    song.name = name
    song.path = path
    session.add(song)
    session.commit()

    return song