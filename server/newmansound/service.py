import logging
from sqlalchemy.sql import func
from newmansound.model import Song, Playlist

logger = logging.getLogger(__name__)


class AudioPlaybackService:
    def __init__(self, player=None):
        """Manages the playback of audio through the computer speakers.
        :param player: PAT Audio Technician instance
        :type player: PAT Audio Technician.
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
        if self._playback_service.get_queue_len() < 100000:
            song = self._playlist_service.dequeue_song()

            if song:
                logger.log(logging.INFO, 'Playing Song %s', song.path)

                try:
                    self._playback_service.queue_song(song)
                except Exception as e:
                    logger.exception(e)


class PlaylistService:
    def __init__(self, session):
        """ Playlist Service
        :param session: SQLAlchemy session to use
        :type session; Session
        """

        self.session = session

    def enqueue_song(self, song_id):
        """ Adds a song to the end of the playlist
        :param song_id: Id of the Song to queue
        :type song_id: int
        """

        max_playlist_query = self.session.query(func.max(Playlist.position).label('max_position'))
        max_playlist_result = max_playlist_query.one()

        max_position = max_playlist_result.max_position

        if max_position is None:
            max_position = 0

        song = self.session.query(Song).get(song_id)

        playlist = Playlist()
        playlist.song = song
        playlist.position = max_position + 1

        self.session.add(playlist)

    def dequeue_song(self):
        """ Retrieves and removes the first song from the playlist
        :returns: The first song from the playlist or None if there are no songs to play.
        :rtype: Song
        """

        playlist_item = self.session.query(Playlist).order_by(Playlist.position).first()

        if playlist_item:
            song = playlist_item.song

            self.session.delete(playlist_item)

            return song
        else:
            return None


class SongService:
    def __init__(self, session):
        """ Song Service
        :param session: SQLAlchemy session to use
        :type session; Session
        """
        self.session = session

    def all(self):
        """Retrieves all songs.
        :returns: A list of all songs.
        :rtype: list of Song
        :"""
        return self.session.query(Song).all()

    def get(self, song_id):
        """Retrieves a song with a given song id.
        :returns: Song for the given song id or None if the song does not exist.
        :rtype: Song"""
        return self.session.query(Song).get(song_id)
