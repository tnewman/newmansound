from sqlalchemy.sql import func

from newmansound.model import Playlist


class AudioPlaybackService:
    def __init__(self, player, media_load_function):
        """Manages the playback of audio through the computer speakers.
        :param player: Pyglet Player used to play audio.
        :type player: pyglet.media.Player
        :param media_load_function: Function used to load audio files.
        :type media_load_function: function
        """

        if player is None:
            import pyglet
            self._player = pyglet.media.Player()
        else:
            self._player = player

        if media_load_function is None:
            import pyglet
            self._media_load_function = pyglet.media.load
        else:
            self._media_load_function = media_load_function

    def play_song(self, song):
        """Play a song through the computer speakers.
        :param song: Song to play
        :type song: Song"""

        media = self._media_load_function(song.path)

        self._player.queue(media)

        if self._player.playing:
            self._player.next_source()
        else:
            self._player.play()


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
