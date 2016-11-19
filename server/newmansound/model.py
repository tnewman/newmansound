from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    artist_id = Column(Integer, ForeignKey('artist.id'))
    artist = relationship('Artist')


class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    album_id = Column(Integer, ForeignKey('album.id'))
    album = relationship('Album')
    path = Column(String)


class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True)
    song_id = Column(Integer, ForeignKey('song.id'))
    position = Column(Integer)
    song = relationship('Song')
