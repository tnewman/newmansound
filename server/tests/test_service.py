import pytest
from unittest.mock import MagicMock

from newmansound.model import Playlist, Song
from newmansound.service import AudioPlaybackService, PlaylistService

from tests.fixtures import engine, session

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

    def test_play_song(self):
        player_mock = MagicMock()

        audio_playback_service = AudioPlaybackService(player_mock, MagicMock())

        song = Song()
        song.path = 'path'

        audio_playback_service._player.playing = False

        audio_playback_service.play_song(song)

        assert 1 == audio_playback_service._player.queue.call_count
        assert 1 == audio_playback_service._player.play.call_count

    def test_play_song_gets_next_source_if_already_playing(self):
        player_mock = MagicMock()

        audio_playback_service = AudioPlaybackService(player_mock, MagicMock())

        song = Song()
        song.path = 'path'

        player_mock.is_playing.return_value = True

        audio_playback_service.play_song(song)

        assert 1 == audio_playback_service._player.queue.call_count
        assert 1 == audio_playback_service._player.next_source.call_count


class TestPlaylistService:

    def test_enqueue_song_adds_with_highest_position(self, session):
        playlist_service = PlaylistService(session)

        song1 = _add_song(session, 'song1')
        song2 = _add_song(session, 'song2')

        _add_playlist(session, song1, 2)

        playlist_service.enqueue_song(song2)

        assert 'song2' == session.query(Playlist).filter_by(position=3).first().song.path

    def test_dequeue_song_returns_song_with_lowest_position(self, session):
        playlist_service = PlaylistService(session)

        song1 = _add_song(session, 'song1')
        song2 = _add_song(session, 'song2')

        _add_playlist(session, song1, 2)
        _add_playlist(session, song2, 1)

        assert song2 == playlist_service.dequeue_song()

    def test_dequeue_song_removes_song_from_queue(self, session):
        playlist_service = PlaylistService(session)

        song = _add_song(session, 'song1')

        _add_playlist(session, song, 1)

        playlist_service.dequeue_song()

        assert None == session.query(Playlist).first()

