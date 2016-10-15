import newmansound.model
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('sqlite:///newmansound.db', convert_unicode=True)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
scoped_session = scoped_session(session)


def init_db():
    """ Initialize SQLAlchemy database tables."""
    newmansound.model.Base.metadata.create_all(bind=engine)
