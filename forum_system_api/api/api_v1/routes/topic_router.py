from fastapi import APIRouter, Response, Query
from fastapi import Depends
from ....schemas.common import FilterParams
from ....schemas.topic import TopicResponse, CreateTopic, TopicUpdate
from ....persistence.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from ....services import topic_service

topic_router = APIRouter(prefix='/topics')


@topic_router.get('/', response_model=list[TopicResponse], status_code=200)
def get_all(
    filter_query: FilterParams = Depends(),
    db: Session = Depends(get_db)
):
    return topic_service.get_all(filter_params=filter_query, db=db)


@topic_router.get('/{topic_id}', response_model=TopicResponse, status_code=200)
def get_by_id(
    topic_id: UUID,
    db: Session = Depends(get_db)
):
    return topic_service.get_by_id(topic_id=topic_id, db=db)


@topic_router.post('/', response_model=TopicResponse, status_code=201)
def create(
    topic: CreateTopic, 
    db: Session = Depends(get_db)
):
    return topic_service.create_topic(topic=topic, db=db)


@topic_router.put('/', response_model=TopicResponse, status_code=200)
def update(
    topic_id: UUID, 
    updated_topic: TopicUpdate, 
    db: Session = Depends(get_db)
):
    return topic_service.update_topic(topic_id=topic_id, updated_topic=updated_topic, db=db)


@topic_router.delete('/', status_code=204)
def delete(
    topic_id: UUID, 
    db: Session = Depends(get_db)
):
    return topic_service.delete_topic(topic_id=topic_id, db=db)