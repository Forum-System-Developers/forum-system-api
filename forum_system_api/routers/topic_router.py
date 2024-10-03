from fastapi import APIRouter, Response
from fastapi import Depends
from ..persistence.database import get_db
from sqlalchemy.orm import Session
from typing import Annotated


db_dependency = Annotated[Session, Depends(get_db)]


topic_router = APIRouter(prefix='/topic')

@topic_router.get('/')
def get_topics():
    pass