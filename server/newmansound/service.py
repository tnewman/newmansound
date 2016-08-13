from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from newmansound.model import Playlist


class PlaylistService:
    def __init__(self, session):
        """
        Playlist Service
        :param session: SQLAlchemy session to use
        """
        self.session = session

    def get_first_song(self):
        """ Retrieves the first song from the playlist
        :returns The first song from the playlist or None if there are no songs to play.
        :rtype Song"""

        playlist_item = self.session.query(Playlist).order_by(Playlist.position).first()
        song = playlist_item.song

        return song
