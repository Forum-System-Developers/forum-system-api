import logging
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.access_level import AccessLevel
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.services.category_service import get_by_id as get_category_by_id
from forum_system_api.services.user_service import is_admin

logger = logging.getLogger(__name__)


def user_permission(
    user: User,
    topic_category_id: UUID,
    db: Session,
) -> bool:
    """
    Determines if a user has permission to access a given topic.

    Args:
        user (User): The user whose permissions are being checked.
        topic_category_id (UUID): The unique identifier of the category associated with the topic.
        db (Session): The database session.

    Returns:
        bool: True if the user has permission to access the topic, False otherwise.
    Raises:
        HTTPException: If the category associated with the topic is not found.
    """
    category = get_category_by_id(category_id=topic_category_id, db=db)
    if not category:
        logger.error(f"Category with ID {topic_category_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    logger.info(f"Retrieved category with ID: {topic_category_id}")

    if category.is_locked:
        logger.info(f"Category with ID {topic_category_id} is locked")
        return is_admin(user_id=user.id, db=db)

    if category.is_private:
        logger.info(f"Category with ID {topic_category_id} is private")
        return category_write_permission(
            user=user, category_id=topic_category_id, db=db
        )

    return True


def get_access_level(
    user: User,
    category_id: UUID,
) -> AccessLevel | None:
    """
    Determines the access level of a user for a specific topic.

    Args:
        user (User): The user whose access level is being checked.
        category_id (UUID): The unique identifier of the category.

    Returns:
        AccessLevel: The access level of the user for the given topic, or None if no matching permission is found.
    """
    access_level = next(
        (
            p.access_level
            for p in user.permissions
            if p.category_id == category_id and p.user_id == user.id
        ),
        None,
    )
    logger.warning(
        f"Retrieved access level {access_level} for user {user.id} in category {category_id} from the database "
        "if it exists or None otherwise"
    )

    return access_level


def category_write_permission(user: User, category_id: UUID, db: Session) -> bool:
    """
    Checks if a user has permission to access a specific category within a topic.

    Args:
        user (User): The user whose permissions are being checked.
        category_id (UUID): The unique identifier of the category.
        db (Session): The database session used for querying.

    Returns:
        bool: True if the user has write access to the category or is an admin, False otherwise.
    """

    user_access = get_access_level(user=user, category_id=category_id)
    write_permission = (
        next(
            (p.category_id for p in user.permissions if p.category_id == category_id),
            None,
        )
        is not None
        and user_access == AccessLevel.WRITE
    ) or is_admin(user_id=user.id, db=db)
    logger.info(f"User {user.id} has write permission: {write_permission}")

    return write_permission


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
        category is not None
        and category.is_private
        and (category.id not in (p.category_id for p in user.permissions))
        and not is_admin(user_id=user.id, db=db)
    ):
        logger.error(
            f"User {user.id} does not have permission to access topic {topic.id}"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
        )
    logger.info(f"User {user.id} has permission to access topic {topic.id}")
