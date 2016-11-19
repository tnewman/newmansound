import json
import pytest
from newmansound.model import Artist, Album, Song
from newmansound.restweb import app, PlaylistService, SongService
from newmansound.schema import SongSchema

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
        song1 = Song()
        song1.name = 'song'
        session.add(song1)

        song2 = Song()
        song2.name = 'song'
        session.add(song2)
        session.commit()

        song_schema = SongSchema()

        songs = song_schema.load(json.loads(client.get('/song').data.decode('utf8')))
        assert len(songs) == 2
