from ..schemas.common import FilterParams
from ..persistence.models.topic import Topic
from ..schemas.topic import TopicResponse, CreateTopic, TopicUpdate
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from fastapi import HTTPException
from uuid import UUID


def get_all(filter_params: FilterParams, db: Session) -> list[TopicResponse]:
    query = (
        db.query(Topic)
        .offset(filter_params.offset)
        .limit(filter_params.limit)
    )
    
    if filter_params.order == 'asc':
        query = query.order_by(asc(getattr(Topic, filter_params.order_by)))
    else:
        query = query.order_by(desc(getattr(Topic, filter_params.order_by)))

    topics = query.all()
    return topics


def get_by_id(topic_id: UUID, db: Session) -> TopicResponse:
    return db.query(Topic).filter(Topic.id == topic_id).first()


def create_topic(topic: CreateTopic, db: Session) -> TopicResponse:
    new_topic = Topic(title = topic.title)
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic


def update_topic(topic_id: UUID, updated_topic: TopicUpdate, db: Session) -> TopicResponse:
    existing_topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not existing_topic:
        raise HTTPException(status_code=404)
    
    if updated_topic.title:
        existing_topic.title = updated_topic.title
        
    if updated_topic.is_locked != existing_topic.is_locked:
        existing_topic.is_locked = updated_topic.is_locked
    
    if updated_topic.best_reply:
        existing_topic.best_reply = updated_topic.best_reply
    
    if updated_topic.category:
        existing_topic.category = updated_topic.category
    
    db.commit()
    db.refresh(existing_topic)
    return existing_topic


def delete_topic(topic_id: UUID, db: Session) -> None:
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404)
    
    db.delete(topic)
    db.commit()