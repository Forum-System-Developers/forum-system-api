from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc, desc

from forum_system_api.schemas.common import FilterParams
from forum_system_api.services.category_service import get_by_id as get_category_by_id
from forum_system_api.services.reply_service import get_by_id as get_reply_by_id
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.schemas.topic import TopicCreate, TopicUpdate


def get_all(filter_params: FilterParams, db: Session) -> list[Topic]:
    query = db.query(Topic)
    
    if filter_params.order:
        if filter_params.order == 'asc':
            query = query.order_by(asc(getattr(Topic, filter_params.order_by)))
        else:
            query = query.order_by(desc(getattr(Topic, filter_params.order_by)))

    query = (query.offset(filter_params.offset)
             .limit(filter_params.limit)
             .all())
    
    return query


def get_by_id(topic_id: UUID, db: Session) -> Topic:
    topic = (db.query(Topic)
            .filter(Topic.id == topic_id)
            .first())
    if topic is None:
        raise HTTPException(status_code=404)
    
    return topic

def create(topic: TopicCreate, user_id: UUID, db: Session) -> Topic:
    category = get_category_by_id(category_id=topic.category_id, db=db)
    if category is None:
        raise HTTPException(status_code=404)
    
    new_topic = Topic(
        author_id = user_id,
        **topic.model_dump()
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic


def update(topic_id: UUID, updated_topic: TopicUpdate, db: Session) -> Topic:
    existing_topic = get_by_id(topic_id=topic_id, db=db)
    best_reply = get_reply_by_id(reply_id=updated_topic.best_reply_id, db=db)
    category = get_category_by_id(category_id=updated_topic.category_id, db=db)
    
    if not all((existing_topic, best_reply, category, updated_topic.title)):
        raise HTTPException(status_code=404, detail='Invalid update request')
    
    if updated_topic.title != existing_topic.title:
        existing_topic.title = updated_topic.title

    if updated_topic.best_reply_id != existing_topic.best_reply_id:
        existing_topic.best_reply_id = updated_topic.best_reply_id

    if updated_topic.category_id != existing_topic.category_id:
        existing_topic.category_id = updated_topic.category_id
    
    db.commit()
    db.refresh(existing_topic)
    return existing_topic


def get_replies(topic_id: UUID, db: Session) -> list[Reply]:
    return (db.query(Reply)
            .options(joinedload(Reply.reactions))
            .filter(Reply.topic_id == topic_id)
            .all())
    