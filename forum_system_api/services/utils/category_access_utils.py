from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.access_level import AccessLevel
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.topic import TopicCreate
from forum_system_api.services.category_service import get_by_id as get_category_by_id
from forum_system_api.services.user_service import is_admin


def user_permission(user: User, topic: Topic | TopicCreate, db: Session) -> bool:
    category = get_category_by_id(category_id=topic.category_id, db=db)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    if category.is_locked:
        return is_admin(user_id=user.id, db=db)

    if category.is_private:
        return category_permission(user=user, topic=topic, db=db)

    return True


def get_access_level(user: User, topic: Topic, db: Session) -> AccessLevel:
    return next(
        (
            p.access_level
            for p in user.permissions
            if p.category_id == topic.category_id and p.user_id == user.id
        ),
        None,
    )


def category_permission(user: User, topic: Topic, db: Session) -> bool:
    user_access = get_access_level(user=user, topic=topic, db=db)
    return (
        next(
            (
                p.category_id
                for p in user.permissions
                if p.category_id == topic.category_id
            ),
            None,
        )
        is not None
        and user_access == AccessLevel.WRITE
    ) or is_admin(user_id=user.id, db=db)


def verify_topic_permission(topic: Topic, user: User, db: Session) -> None:
    category = get_category_by_id(category_id=topic.category_id, db=db)
    if category.is_private and (category.id not in [p.category_id for p in user.permissions]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
            )
