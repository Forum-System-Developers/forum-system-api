from typing import Literal
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.orm import Session, joinedload

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.category import Category
from forum_system_api.schemas.common import TopicFilterParams
from forum_system_api.schemas.topic import TopicCreate, TopicUpdate
from forum_system_api.services.reply_service import get_by_id as get_reply_by_id
from forum_system_api.services.user_service import is_admin
from forum_system_api.services.utils.category_access_utils import (
    user_permission,
    verify_topic_permission,
)


def get_all(filter_params: TopicFilterParams, user: User, db: Session) -> list[Topic]:
    category_ids = [p.category_id for p in user.permissions]
    query = db.query(Topic).join(Category, Topic.category_id == Category.id)

    # gets all categories that are not private
    # or those that are private, but in user permissions
    query = query.filter(
        or_(
            and_(Category.is_private, Topic.category_id.in_(category_ids)),
            Topic.author_id == user.id,
            not Category.is_private,
            is_admin(user_id=user.id, db=db),
        )
    )

    if filter_params.order:
        order_by = asc if filter_params.order == "asc" else desc
        query = query.order_by(order_by(getattr(Topic, filter_params.order_by)))

    query = query.offset(filter_params.offset).limit(filter_params.limit).all()

    return query


def get_by_id(topic_id: UUID, user: User, db: Session) -> Topic:
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
        )
        
    if not is_admin(user_id=user.id, db=db):
        verify_topic_permission(topic=topic, user=user, db=db)

    return topic


def get_by_title(title: str, db: Session) -> Topic | None:
    return db.query(Topic).filter(Topic.title == title).first()


def create(topic: TopicCreate, user: User, db: Session) -> Topic:
    if not user_permission(user=user, topic=topic, db=db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to do that",
        )
    if get_by_title(title=topic.title, db=db) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Topic with this title already exists, please select a new title",
        )

    new_topic = Topic(author_id=user.id, **topic.model_dump())
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic


def update(
    user: User, topic_id: UUID, updated_topic: TopicUpdate, db: Session
) -> Topic:
    topic = _validate_topic_access(topic_id=topic_id, user=user, db=db)
    if not user_permission(user=user, topic=topic, db=db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to do that",
        )

    if updated_topic.title and updated_topic.title != topic.title:
        topic.title = updated_topic.title

    if updated_topic.category_id and updated_topic.category_id != topic.category_id:
        topic.category_id = updated_topic.category_id

    if any((updated_topic.title, updated_topic.category_id)):
        db.commit()
        db.refresh(topic)
        
    return topic


def get_replies(topic_id: UUID, db: Session) -> list[Reply]:
    return (
        db.query(Reply)
        .options(joinedload(Reply.reactions))
        .filter(Reply.topic_id == topic_id)
        .all()
    )


def lock(user: User, topic_id: Topic, lock_topic: bool, db: Session) -> Topic:
    topic = get_by_id(topic_id=topic_id, user=user, db=db)
    topic.is_locked = lock_topic
    db.commit()
    db.refresh(topic)
    return topic


def select_best_reply(user: User, topic_id: UUID, reply_id: UUID, db: Session) -> Topic:
    topic = _validate_topic_access(topic_id=topic_id, user=user, db=db)
    reply = get_reply_by_id(reply_id=reply_id, db=db)

    topic.best_reply_id = reply_id
    db.commit()
    db.refresh(topic)
    return topic


def _validate_topic_access(topic_id: UUID, user: User, db: Session) -> Topic:
    topic = get_by_id(topic_id=topic_id, user=user, db=db)
    if topic.author_id != user.id and not is_admin(user_id=user.id, db=db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
        )

    if topic.is_locked and not is_admin(user_id=user.id, db=db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Topic is locked"
        )

    return topic
