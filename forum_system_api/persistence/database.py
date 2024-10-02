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


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from forum_system_api.persistence.models import (
        user, 
        category, 
        category_permission,
        conversation, 
        message, 
        reply, 
        reply_reaction, 
        topic
    )
    Base.metadata.create_all(bind=engine)
