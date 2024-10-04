from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from ....schemas.common import FilterParams
from ....schemas.topic import TopicResponse, TopicCreate, TopicUpdate
from ....persistence.database import get_db
from ....services import topic_service


topic_router = APIRouter(prefix='/topics', tags=["topics"])


@topic_router.get('/', response_model=list[TopicResponse], status_code=200)
def get_all(
    filter_query: FilterParams = Depends(),
    db: Session = Depends(get_db)
) -> list[TopicResponse]:
    return topic_service.get_all(filter_params=filter_query, db=db)


@topic_router.get('/{topic_id}', response_model=TopicResponse, status_code=200)
def get_by_id(
    topic_id: UUID,
    db: Session = Depends(get_db)
) -> TopicResponse:
    topic = topic_service.get_by_id(topic_id=topic_id, db=db)
    if topic is None:
        raise HTTPException(status_code=404)
    return topic
    

@topic_router.post('/', response_model=TopicResponse, status_code=201)
def create(
    topic: TopicCreate, 
    db: Session = Depends(get_db)
) -> TopicResponse:
    topic = topic_service.create(topic=topic, db=db)
    if topic is None:
        raise HTTPException(status_code=404)
    return topic


@topic_router.put('/', response_model=TopicResponse, status_code=200)
def update(
    topic_id: UUID, 
    updated_topic: TopicUpdate, 
    db: Session = Depends(get_db)
) -> TopicResponse:
    topic = topic_service.update(topic_id=topic_id, updated_topic=updated_topic, db=db)
    if topic is None:
        raise HTTPException(status_code=404, detail='Topic not found')
    return topic