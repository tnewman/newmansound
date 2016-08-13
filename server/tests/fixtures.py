import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from newmansound.model import Base


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
