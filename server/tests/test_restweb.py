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

        assert playlist_service.dequeue_song().path == 'newsong'

    def test_post_status_400_on_bad_data(self, client, playlist_service, session):
        assert client.post('/playlist', data=json.dumps({}), content_type='application/json').status_code == 400


class TestSongList:

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


class TestSong:

    def test_get_returns_song_with_a_given_id(self, client, session):
        song1 = Song()
        song1.name = 'song'
        session.add(song1)
        session.commit()

        song_schema = SongSchema()
        song = song_schema.load(json.loads(client.get('/song/' + str(song1.id)).data.decode('utf8')))
        assert song.data['name'] == 'song'

    def test_get_returns_404_for_invalid_id(self, client, session):
        assert client.get('/song/invalid').status_code == 404