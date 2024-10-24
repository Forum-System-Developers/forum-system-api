from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from forum_system_api.config import DATABASE_URL


Base = declarative_base()

engine = create_engine(DATABASE_URL, echo=True)

session_local = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

from forum_system_api.persistence.models import (
    admin, 
    user, 
    category, 
    user_category_permission, 
    message, 
    conversation, 
    reply, 
    reply_reaction, 
    topic
)


def get_db():
    """
    Provides a database session for use in a context manager.

    Yields:
        db: A database session object.

    Ensures that the database session is properly closed after use.
    """
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all tables in the database.

    This function uses SQLAlchemy's metadata to create all tables that are defined
    in the Base class. It binds the metadata to the specified engine and creates
    the tables if they do not already exist.

    Returns:
        None
    """
    Base.metadata.create_all(bind=engine)
