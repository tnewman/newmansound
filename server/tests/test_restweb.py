import json
import pytest
from newmansound.model import Artist, Album, Song
from newmansound.restweb import app, PlaylistService, SongService

from tests.fixtures import client, engine, playlist_service, session


class TestPlaylistRequest:

    def test_post_creates_playlist_request(self, client, playlist_service, session):
        song = Song()
        song.path = 'newsong'
        session.add(song)
        session.commit()

        client.post('/playlist', data=json.dumps({'id': song.id}), content_type='application/json')

        assert playlist_service.peek_song().path == 'newsong'


class TestSongRequest:

    def test_get_returns_list_of_songs(self, client, session):
        song = Song()
        song.name = 'song'
        session.add(song)
        session.commit()

        song_service = SongService(session)

        assert song_service.all()[0].name == 'song'