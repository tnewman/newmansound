import logging
from sqlalchemy.sql import func
from newmansound.model import Playlist

logger = logging.getLogger(__name__)


class AudioPlaybackService:
    def __init__(self, player=None):
        """Manages the playback of audio through the computer speakers.
        :type player: PAT Audio Technician instance.
        :param media_load_function: Function used to load audio files.
        :type media_load_function: function
        """

        if player is None:
            import pat
            self._player = pat
        else:
            self._player = player

    def queue_song(self, song):
        """Play a song through the computer speakers.
        :param song: Song to play
        :type song: Song"""

        self._player.queue(song.path)

    def get_queue_len(self):
        """Get the number of bytes still queued for playback.
        :return: The number of bytes of audio still queued.
        :rtype: int"""

        return self._player.get_queue_len()


class JukeboxService:
    def __init__(self, playback_service, playlist_service):
        """ Coordinates the jukebox. Responsible for dequeing music from the playlist and playing it over the
        speakers.
        :param playback_service: AudioPlaybackService instance that will play audio over the speakers.
        :type playback_service: AudioPlaybackService
        :param playlist_service: PlaylistService instance that will provide the queue of songs to play.
        :type playlist_service: PlaylistService"""

        self._playback_service = playback_service
        self._playlist_service = playlist_service

    def play_next_song(self):
        peek_song = self._playlist_service.peek_song()

        if not peek_song is None:
            if self._playback_service.get_queue_len() < 100000:
                song = self._playlist_service.dequeue_song()
                logger.log(logging.INFO, 'Playing Song %s', peek_song.path)
                self._playback_service.queue_song(peek_song)


class PlaylistService:
    def __init__(self, session):
        """ Playlist Service
        :param session: SQLAlchemy session to use
        :type session; Session
        """

        self.session = session

    def enqueue_song(self, song):
        """ Adds a song to the end of the playlist
        :param song: Song to queue
        :type song: Song
        """

        query = self.session.query(func.max(Playlist.position).label('max_position'))
        result = query.one()

        max_position = result.max_position

        playlist = Playlist()
        playlist.song = song
        playlist.position = max_position + 1

        self.session.add(playlist)

    def dequeue_song(self):
        """ Retrieves and removes the first song from the playlist
        :returns: The first song from the playlist or None if there are no songs to play.
        :rtype: Song
        """

        return self._retrieve_song(True)

    def peek_song(self):
        """Retrives the first song from the playlist without removing it
        :returns: The first song from the playlist or None if there are no songs to play.
        :rtype: Song"""

        return self._retrieve_song(False)

    def _retrieve_song(self, delete):
        playlist_item = self.session.query(Playlist).order_by(Playlist.position).first()

        if playlist_item:
            song = playlist_item.song

            if delete:
                self.session.delete(playlist_item)

            return song
        else:
            return None