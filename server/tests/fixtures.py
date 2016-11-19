import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import MagicMock

import newmansound.database
import newmansound.model
from newmansound.restweb import app
from newmansound.service import AudioPlaybackService, JukeboxService, PlaylistService


@pytest.fixture(scope='function')
def audio_playback_service():
    """Creates an Audio Playback Service with a mock Media Player and Media Loader."""

    pat_mock = MagicMock(autospec=True)
    pat_mock.get_queue_len.return_value = 0

    playback_service = AudioPlaybackService(pat_mock)

    return playback_service


@pytest.fixture(scope='session')
def engine():
    """Creates an in-memory SQLAlchemy database engine that will be created once and reused for all tests."""

    in_memory_engine = create_engine('sqlite:///:memory:')
    newmansound.database.engine = in_memory_engine
    newmansound.database.init_db()

    return in_memory_engine


@pytest.fixture(scope='function')
def session(request, engine):
    """Creates a new SQLAlchemy Session for each test that will be rolled back after each test execution."""
    connection = engine.connect()
    transaction = connection.begin()
    session_class = sessionmaker(bind=connection)
    session = session_class()

    def finalizer():
        transaction.rollback()
        session.close()
        connection.close()

    request.addfinalizer(finalizer)

    app.session = session

    return session


@pytest.fixture(scope='function')
def playlist_service(session):
    """Creates a new Playlist Service with a SQLAlchemy session that will be rolled back after each test and a mock
    audio player."""

    return PlaylistService(session)


@pytest.fixture(scope='function')
def jukebox_service(audio_playback_service, playlist_service):
    """Creates a new Jukebox Service with a SQLAlchemy session that will be rolled back after each test and a mock
    audio player."""

    return JukeboxService(audio_playback_service, playlist_service)

@pytest.fixture(scope='function')
def client(playlist_service):
    """ Creates a Flask client"""

    return app.test_client()