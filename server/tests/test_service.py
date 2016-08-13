import pytest

from tests.fixtures import engine, session

from newmansound.model import Playlist, Song
from newmansound.service import PlaylistService

def _add_song(session, path):
    song = Song()
    song.path = path
    session.add(song)

    return song

def _add_playlist(session, song, position):
    playlist = Playlist()
    playlist.song = song
    playlist.position = position
    session.add(playlist)

class TestPlaylistService:

    def test_get_first_song_returns_song_with_lowest_position(self, session):
        playlist_service = PlaylistService(session)

        song1 = _add_song(session, 'song1')
        song2 = _add_song(session, 'song2')

        _add_playlist(session, song1, 2)
        _add_playlist(session, song2, 1)

        assert song2 == playlist_service.get_first_song()

    def test_add_song_adds_with_highest_position(self, session):
        playlist_service = PlaylistService(session)

        song1 = _add_song(session, 'song1')
        song2 = _add_song(session, 'song2')

        _add_playlist(session, song1, 2)

        playlist_service.add_song(song2)

        assert 'song2' == session.query(Playlist).filter_by(position=3).first().song.path
