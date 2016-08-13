import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from newmansound.model import Base


@pytest.fixture(scope='session')
def engine():
    in_memory_engine = create_engine('sqlite:///:memory:')

    Base.metadata.create_all(bind=in_memory_engine)

    return in_memory_engine


@pytest.fixture(scope='function')
def session(request, engine):
    session_class = sessionmaker(bind=engine)
    session = session_class()

    def finalizer():
        session.rollback()
        session.close()

    request.addfinalizer(finalizer)

    return session
