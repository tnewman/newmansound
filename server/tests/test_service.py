import pytest

from tests.fixtures import engine, session

from newmansound.model import Playlist, Song
from newmansound.service import PlaylistService


def test_song_service_first_song_returns_first_song(session):
    song_service = PlaylistService(session)

    song1 = Song()
    song1.path = 'song1'
    session.add(song1)

    song2 = Song()
    song2.path = 'song2'
    session.add(song2)

    playlist1 = Playlist()
    playlist1.song = song1
    playlist1.position = 2
    session.add(playlist1)

    playlist2 = Playlist()
    playlist2.song = song2
    playlist2.position = 1
    session.add(playlist2)

    assert song2 == song_service.get_first_song()
