from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.orm import Session, joinedload

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.category import Category
from forum_system_api.persistence.models.user_category_permission import (
    UserCategoryPermission,
)
from forum_system_api.schemas.common import TopicFilterParams
from forum_system_api.schemas.topic import TopicCreate, TopicLock, TopicUpdate
from forum_system_api.services.reply_service import get_by_id as get_reply_by_id
from forum_system_api.services.user_service import is_admin
from forum_system_api.services.utils.category_access_utils import user_permission


def get_all(filter_params: TopicFilterParams, user: User, db: Session) -> list[Topic]:

    # checks for user permissions
    user_permissions_subquery = (
        db.query(UserCategoryPermission.category_id)
        .filter(UserCategoryPermission.user_id == user.id)
        .subquery()
    )

    query = db.query(Topic).join(Category, Topic.category_id == Category.id)

    # gets all categories that are not provate and those that are private, but in user permissions
    query = query.filter(
        or_(
            Category.is_private == False,
            and_(
                Category.is_private == True,
                Topic.category_id.in_(user_permissions_subquery),
            ),
            Topic.author_id == user.id,
            is_admin(user_id=user.id, db=db),
        )
    )

    if filter_params.order:
        if filter_params.order == "asc":
            query = query.order_by(asc(getattr(Topic, filter_params.order_by)))
        else:
            query = query.order_by(desc(getattr(Topic, filter_params.order_by)))

    query = query.offset(filter_params.offset).limit(filter_params.limit).all()

    return query


def get_by_id(topic_id: UUID, user: User, db: Session) -> Topic:
    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
        )

    return topic


def get_by_name(title: str, db: Session) -> Topic:
    return db.query(Topic).filter(Topic.title == title).first()


def create(topic: TopicCreate, user: User, db: Session) -> Topic:
    if not user_permission(user=user, topic=topic, db=db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to do that",
        )
    if get_by_name(title=topic.title, db=db) is not None:
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
    topic = validate_topic_access(topic_id=topic_id, user=user, db=db)
    if not user_permission(user=user, topic=topic, db=db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to do that",
        )

    if (
        updated_topic.best_reply_id
        and updated_topic.best_reply_id != topic.best_reply_id
    ):
        reply = get_reply_by_id(reply_id=updated_topic.best_reply_id, db=db)
        topic.best_reply_id = reply.id

    if updated_topic.title != topic.title and updated_topic.title is not None:
        topic.title = updated_topic.title

    if updated_topic.category_id != topic.category_id:
        topic.category_id = updated_topic.category_id

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


def lock(topic_id: Topic, lock_topic: TopicLock, db: Session) -> Topic:
    topic = get_by_id(topic_id=topic_id, db=db)
    topic.is_locked = lock_topic.is_locked
    db.commit()
    db.refresh(topic)
    return topic


def select_best_reply(user: User, topic_id: UUID, reply_id: UUID, db: Session) -> Topic:
    topic = validate_topic_access(topic_id=topic_id, user=user, db=db)
    reply = get_reply_by_id(reply_id=reply_id, db=db)

    topic.best_reply_id = reply_id
    db.commit()
    db.refresh(topic)
    return topic


def validate_topic_access(topic_id: UUID, user: User, db: Session) -> Topic:
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
