import pytest
import pyglet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock

from newmansound.model import Base
from newmansound.service import AudioPlaybackService


@pytest.fixture(scope='function')
def audio_playback_service():
    """Creates an Audio Playback Service with a mock Media Player and Media Loader."""

    mock_media_player = MagicMock(spec=pyglet.media.Player)
    mock_media_loader = MagicMock(spec=pyglet.media.load)

    playback_service = AudioPlaybackService(mock_media_player, mock_media_loader)

    return playback_service


@pytest.fixture(scope='session')
def engine():
    """Creates an in-memory SQLAlchemy database engine that will be created once and reused for all tests."""

    in_memory_engine = create_engine('sqlite:///:memory:')

    Base.metadata.create_all(bind=in_memory_engine)

    return in_memory_engine


@pytest.fixture(scope='function')
def session(request, engine):
    """Creates a new SQLAlchemy Session for each test that will be rolled back after each test execution."""

    session_class = sessionmaker(bind=engine)
    session = session_class()

    def finalizer():
        session.rollback()
        session.close()

    request.addfinalizer(finalizer)

    return session
