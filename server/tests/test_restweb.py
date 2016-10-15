import pytest
from newmansound.model import Song
from newmansound.restweb import app, PlaylistService

from tests.fixtures import client, engine, playlist_service, session


class TestPlaylistRequest:

    def test_post_creates_playlist_request(self, client, playlist_service, session):
        song = Song()
        song.path = 'newsong'
        session.add(song)
        session.commit()

        client.post('/playlist', data={'song_id': song.id})

        assert playlist_service.peek_song().id == 1
