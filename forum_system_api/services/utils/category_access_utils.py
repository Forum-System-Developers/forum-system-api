from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.access_level import AccessLevel
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.topic import TopicCreate
from forum_system_api.services.category_service import get_by_id as get_category_by_id
from forum_system_api.services.user_service import is_admin


def user_permission(user: User, topic: Topic | TopicCreate, db: Session) -> bool:
    """
    Determines if a user has permission to access a given topic.

    Args:
        user (User): The user whose permissions are being checked.
        topic (Topic | TopicCreate): The topic or topic creation data.
        db (Session): The database session.
    Returns:
        bool: True if the user has permission to access the topic, False otherwise.
    Raises:
        HTTPException: If the category associated with the topic is not found.
    """

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
    """
    Determines the access level of a user for a specific topic.

    Args:
        user (User): The user whose access level is being checked.
        topic (Topic): The topic for which the access level is being determined.
        db (Session): The database session used for querying.

    Returns:
        AccessLevel: The access level of the user for the given topic, or None if no matching permission is found.
    """

    return next(
        (
            p.access_level
            for p in user.permissions
            if p.category_id == topic.category_id and p.user_id == user.id
        ),
        None,
    )


def category_permission(user: User, topic: Topic, db: Session) -> bool:
    """
    Checks if a user has permission to access a specific category within a topic.

    Args:
        user (User): The user whose permissions are being checked.
        topic (Topic): The topic that contains the category.
        db (Session): The database session used for querying.

    Returns:
        bool: True if the user has write access to the category or is an admin, False otherwise.
    """

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
    """
    Verifies if a user has permission to access a specific topic.

    Args:
        topic (Topic): The topic to verify access for.
        user (User): The user whose permissions are being checked.
        db (Session): The database session used for querying.

    Raises:
        HTTPException: If the user does not have permission to access the topic.
    """

    category = get_category_by_id(category_id=topic.category_id, db=db)
    if (
        category.is_private
        and (category.id not in [p.category_id for p in user.permissions])
        and not is_admin(user_id=user.id, db=db)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
        )
