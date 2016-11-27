from newmansound.model import Album, Artist, Song
from tests.fixtures import engine, session


def add_album(session, name=''):
    album = Album()
    album.name = name
    session.add(album)
    session.commit()

    return album


def add_artist(session, name=''):
    artist = Artist()
    artist.name = name
    session.add(artist)
    session.commit()

    return artist


def add_song(session, path='', name=''):
    song = Song()
    song.name = name
    song.path = path
    session.add(song)
    session.commit()

    return song