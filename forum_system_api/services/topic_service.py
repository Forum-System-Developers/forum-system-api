from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from forum_system_api.schemas.common import FilterParams
from .category_service import get_by_id as get_category_by_id
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.schemas.topic import TopicCreate, TopicUpdate


def get_all(filter_params: FilterParams, db: Session) -> list[Topic]:
    query = db.query(Topic)
    
    if filter_params.order:
        if filter_params.order == 'asc':
            query = query.order_by(asc(getattr(Topic, filter_params.order_by)))
        else:
            query = query.order_by(desc(getattr(Topic, filter_params.order_by)))

    query = query.offset(filter_params.offset).limit(filter_params.limit)
    return query.all()


def get_by_id(topic_id: UUID, db: Session) -> Topic:
    topic = (db.query(Topic)
            .filter(Topic.id == topic_id)
            .one_or_none())
    if topic is None:
        raise HTTPException(status_code=404)
    
    return topic

def create(topic: TopicCreate, db: Session) -> Topic:
    category = get_category_by_id(category_id=topic.category_id, db=db)
    if category is None:
        raise HTTPException(status_code=404)
    
    new_topic = Topic(
        **topic.model_dump()
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic


def update(topic_id: UUID, updated_topic: TopicUpdate, db: Session) -> Topic:
    existing_topic = get_by_id(topic_id=topic_id, db=db)
    
    if existing_topic is None:
        raise HTTPException(status_code=404, detail='Topic not found')
    
    if updated_topic.title is not None:
        existing_topic.title = updated_topic.title
        
    if updated_topic.is_locked != existing_topic.is_locked:
        existing_topic.is_locked = updated_topic.is_locked
    
    if updated_topic.best_reply is not None:
        existing_topic.best_reply = updated_topic.best_reply
    
    if updated_topic.category is not None:
        existing_topic.category = updated_topic.category
    
    db.commit()
    db.refresh(existing_topic)
    return existing_topic
