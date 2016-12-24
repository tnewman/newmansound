import json
import pytest
from newmansound.model import Artist, Album, Song
from newmansound.restweb import app, PlaylistService, SongService
from newmansound.schema import AlbumSchema, SongSchema

from tests.fixtures import client, engine, playlist_service, session
from tests.helpers import add_album, add_song


class TestAlbumList:

    def test_get_returns_list_of_albums(self, client, session):
        add_album(session)
        add_album(session)

        album_schema = AlbumSchema()

        albums = album_schema.load(json.loads(client.get('/album').data.decode('utf8')))
        assert len(albums) == 2


class TestAlbum:

    def test_get_returns_album_with_a_given_id(self, client, session):
        album1 = add_album(session, name='album')

        album_schema = AlbumSchema()
        album = album_schema.load(json.loads(client.get('/album/' + str(album1.id)).data.decode('utf8')))
        assert album.data['name'] == 'album'


class TestPlaylistRequest:

    def test_post_creates_playlist_request(self, client, playlist_service, session):
        song = add_song(session, path='newsong')

        client.post('/playlist', data=json.dumps({'id': song.id}), content_type='application/json')

        assert playlist_service.dequeue_song().path == 'newsong'

    def test_post_status_400_on_bad_data(self, client, playlist_service, session):
        assert client.post('/playlist', data=json.dumps({}), content_type='application/json').status_code == 400


class TestSongList:

    def test_get_returns_list_of_songs(self, client, session):
        add_song(session)
        add_song(session)

        song_schema = SongSchema()

        songs = song_schema.load(json.loads(client.get('/song').data.decode('utf8')))
        assert len(songs) == 2


class TestSong:

    def test_get_returns_song_with_a_given_id(self, client, session):
        song1 = add_song(session, name='song')

        song_schema = SongSchema()
        song = song_schema.load(json.loads(client.get('/song/' + str(song1.id)).data.decode('utf8')))
        assert song.data['name'] == 'song'

    def test_get_returns_404_for_invalid_id(self, client, session):
        assert client.get('/song/invalid').status_code == 404