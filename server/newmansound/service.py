from sqlalchemy.sql import func

from newmansound.model import Playlist


class PlaylistService:
    def __init__(self, session):
        """ Playlist Service
        :param session: SQLAlchemy session to use
        """
        self.session = session

    def get_first_song(self):
        """ Retrieves the first song from the playlist
        :returns: The first song from the playlist or None if there are no songs to play.
        :rtype: Song
        """

        playlist_item = self.session.query(Playlist).order_by(Playlist.position).first()
        song = playlist_item.song

        return song

    def add_song(self, song):
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
