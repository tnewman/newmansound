import pytest

from newmansound.model import Playlist, Song
from newmansound.service import JukeboxService, PlaylistService, SongService

from tests.fixtures import audio_playback_service, playlist_service, engine, session


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


class TestAudioPlaybackService:

    def test_queue_song_queues_song_for_playback(self, audio_playback_service):
        song = Song()
        song.path = 'path'

        audio_playback_service.queue_song(song)

        assert 1 == audio_playback_service._player.queue.call_count

    def test_get_bytes_queued_returns_bytes_queued(self, audio_playback_service):
        audio_playback_service._player.get_queue_len.return_value = 1024

        assert 1024 == audio_playback_service.get_queue_len()


class TestJukeboxService:

    def test_jukebox_service_plays_song(self, audio_playback_service, playlist_service, session):
        jukebox_service = JukeboxService(audio_playback_service, playlist_service)

        song = _add_song(session, 'song')
        _add_playlist(session, song, 1)

        jukebox_service.play_next_song()

        audio_playback_service._player.queue.assert_called_with('song')

    def test_jukebox_service_does_not_play_none_song(self, audio_playback_service, playlist_service, session):
        jukebox_service = JukeboxService(audio_playback_service, playlist_service)

        jukebox_service.play_next_song()

        assert 0 == audio_playback_service._player.queue.call_count

    def test_jukebox_service_does_not_queue_until_buffer_is_low(self, audio_playback_service, playlist_service,
                                                                session):
        jukebox_service = JukeboxService(audio_playback_service, playlist_service)

        audio_playback_service._player.get_queue_len.return_value = 1000000

        song = _add_song(session, 'song')
        _add_playlist(session, song, 1)

        jukebox_service.play_next_song()

        assert 0 == audio_playback_service._player.queue.call_count

    def test_jukebox_service_does_not_dequeue_songs_when_buffer_high(self, audio_playback_service, playlist_service,
                                                                     session):
        jukebox_service = JukeboxService(audio_playback_service, playlist_service)

        song = _add_song(session, 'song')
        _add_playlist(session, song, 1)

        audio_playback_service._player.get_queue_len.return_value = 1000000

        jukebox_service.play_next_song()

        audio_playback_service._player.get_queue_len.return_value = 50000

        jukebox_service.play_next_song()

        assert 1 == audio_playback_service._player.queue.call_count

    def test_jukebox_service_dequeues_garbage_from_playlist(self, audio_playback_service, playlist_service, session):
        jukebox_service = JukeboxService(audio_playback_service, playlist_service)

        _add_playlist(session, None, 1)
        _add_playlist(session, None, 1)
        _add_playlist(session, None, 1)
        _add_playlist(session, None, 1)

        jukebox_service.play_next_song()

        assert playlist_service.peek_song() is None


class TestSongService:

    def test_song_service_returns_all_songs(self, session):
        song_service = SongService(session)

        song1 = _add_song(session, 'song1')
        song2 = _add_song(session, 'song2')

        assert song_service.all()[0].path == 'song1'
        assert len(song_service.all()) == 2


class TestPlaylistService:

    def test_enqueue_song_adds_with_highest_position(self, session):
        playlist_service = PlaylistService(session)

        song1 = _add_song(session, 'song1')
        song2 = _add_song(session, 'song2')
        session.commit()

        _add_playlist(session, song1, 2)

        playlist_service.enqueue_song(song2.id)

        assert 'song2' == session.query(Playlist).filter_by(position=3).first().song.path

    def test_enqueue_uses_position_1_when_playlist_empty(self, session):
        playlist_service = PlaylistService(session)

        song1 = _add_song(session, 'song1')
        session.commit()

        playlist_service.enqueue_song(song1.id)

        assert 1 == session.query(Playlist).first().position

    def test_peek_song_returns_song_with_lowest_position(self, session):
        playlist_service = PlaylistService(session)

        song1 = _add_song(session, 'song1')
        song2 = _add_song(session, 'song2')

        _add_playlist(session, song1, 2)
        _add_playlist(session, song2, 1)

        assert song2 == playlist_service.peek_song()

    def test_peek_song_returns_none_on_empty_playlist(self, session):
        playlist_service = PlaylistService(session)

        assert None is playlist_service.peek_song()

    def test_peek_song_does_not_remove_song_from_queue(self, session):
        playlist_service = PlaylistService(session)

        song = _add_song(session, 'song1')

        _add_playlist(session, song, 1)

        playlist_service.peek_song()

        assert not None is session.query(Playlist).first()

    def test_dequeue_song_returns_song_with_lowest_position(self, session):
        playlist_service = PlaylistService(session)

        song1 = _add_song(session, 'song1')
        song2 = _add_song(session, 'song2')

        _add_playlist(session, song1, 2)
        _add_playlist(session, song2, 1)

        assert song2 == playlist_service.dequeue_song()

    def test_dequeue_song_returns_none_on_empty_playlist(self, session):
        playlist_service = PlaylistService(session)

        assert None is playlist_service.peek_song()

    def test_dequeue_song_removes_song_from_queue(self, session):
        playlist_service = PlaylistService(session)

        song = _add_song(session, 'song1')

        _add_playlist(session, song, 1)

        playlist_service.dequeue_song()

        assert None is session.query(Playlist).first()
