from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session, joinedload

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.common import FilterParams
from forum_system_api.schemas.topic import TopicCreate, TopicLock, TopicUpdate
from forum_system_api.services.category_service import get_by_id as get_category_by_id
from forum_system_api.services.reply_service import get_by_id as get_reply_by_id


def get_all(filter_params: FilterParams, db: Session) -> list[Topic]:
    query = db.query(Topic)

    if filter_params.order:
        if filter_params.order == "asc":
            query = query.order_by(asc(getattr(Topic, filter_params.order_by)))
        else:
            query = query.order_by(desc(getattr(Topic, filter_params.order_by)))

    query = query.offset(filter_params.offset).limit(filter_params.limit).all()

    return query


def get_by_id(topic_id: UUID, db: Session) -> Topic:
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if topic is None:
        raise HTTPException(status_code=404)

    return topic


def create(topic: TopicCreate, user_id: UUID, db: Session) -> Topic:
    category = get_category_by_id(category_id=topic.category_id, db=db)
    if category is None:
        raise HTTPException(status_code=404)

    new_topic = Topic(author_id=user_id, **topic.model_dump())
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic


def update(
    user: User, topic_id: UUID, updated_topic: TopicUpdate, db: Session
) -> Topic:
    existing_topic = get_by_id(topic_id=topic_id, db=db)
    if existing_topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")

    if existing_topic.author_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    reply = get_reply_by_id(reply_id=updated_topic.best_reply_id, db=db)
    category = get_category_by_id(category_id=updated_topic.category_id, db=db)
    if reply is None or category is None:
        raise HTTPException(status_code=404, detail="Invalid update request")

    if updated_topic.title != existing_topic.title and updated_topic.title is not None:
        existing_topic.title = updated_topic.title

    if updated_topic.best_reply_id != existing_topic.best_reply_id:
        existing_topic.best_reply_id = reply.id

    if updated_topic.category_id != existing_topic.category_id:
        existing_topic.category_id = updated_topic.category_id

    db.commit()
    db.refresh(existing_topic)
    return existing_topic


def get_replies(topic_id: UUID, db: Session) -> list[Reply]:
    return (
        db.query(Reply)
        .options(joinedload(Reply.reactions))
        .filter(Reply.topic_id == topic_id)
        .all()
    )


def lock(topic_id: UUID, lock_topic: TopicLock, db: Session) -> Topic:
    topic = get_by_id(topic_id=topic_id, db=db)
    topic.is_locked = lock_topic.is_locked
    db.commit()
    db.refresh(topic)
    return topic


def select_best_reply(user: User, topic_id: UUID, reply_id: UUID, db: Session) -> Topic:
    topic = get_by_id(topic_id=topic_id, db=db)
    if user.id != topic.author_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    reply = get_reply_by_id(reply_id=reply_id, db=db)
    if reply is None:
        raise HTTPException(status_code=404, detail="Reply does not exist")

    topic.best_reply_id = reply_id
    db.commit()
    db.refresh(topic)
    return topic
