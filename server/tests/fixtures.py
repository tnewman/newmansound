import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock

from newmansound.model import Base
from newmansound.service import AudioPlaybackService, PlaylistService


@pytest.fixture(scope='function')
def audio_playback_service():
    """Creates an Audio Playback Service with a mock Media Player and Media Loader."""

    pat_mock = MagicMock()

    playback_service = AudioPlaybackService(pat_mock)

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


@pytest.fixture(scope='function')
def playlist_service(session):
    """Creates a new Playlist Service with a SQLAlchemy session that will be rolled back after each test and a mock
    ."""

    return PlaylistService(session)
