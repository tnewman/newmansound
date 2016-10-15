from sqlalchemy.sql import func

from newmansound.model import Playlist


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
        """ Retrieves the first song from the playlist
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
