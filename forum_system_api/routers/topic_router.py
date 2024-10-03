from fastapi import APIRouter, Response, Query
from fastapi import Depends
from ..schemas.common import FilterParams
from ..schemas.topic import TopicResponse
from ..persistence.database import get_db
from sqlalchemy.orm import Session
from ..services import topic_service

topic_router = APIRouter(prefix='/topics')


@topic_router.get('/', response_model=list[TopicResponse], status_code=200)
def get_topics(
    filter_query: FilterParams = Depends(),
    db: Session = Depends(get_db)
):
    return topic_service.get_all(filter_params=filter_query, db=db)