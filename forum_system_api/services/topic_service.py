from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import and_, asc, desc, or_
from sqlalchemy.orm import Session, joinedload

from forum_system_api.persistence.models.category import Category
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.common import TopicFilterParams
from forum_system_api.schemas.topic import TopicCreate, TopicUpdate
from forum_system_api.services.reply_service import get_by_id as get_reply_by_id
from forum_system_api.services.user_service import is_admin
from forum_system_api.services.utils.category_access_utils import (
    user_permission,
    verify_topic_permission,
)


def get_all(filter_params: TopicFilterParams, user: User, db: Session) -> list[Topic]:
    """
    Retrieve all topics based on filter parameters and user permissions.

    Args:
        filter_params (TopicFilterParams): Parameters to filter and sort the topics.
        user (User): The user requesting the topics.
        db (Session): The database session.
    Returns:
        list[Topic]: A list of topics that match the filter criteria and user permissions.
    """

    category_ids = {p.category_id for p in user.permissions}
    query = db.query(Topic).join(Category, Topic.category_id == Category.id)

    # gets all categories that are not private
    # or those that are private, but in user permissions
    query = query.filter(
        or_(
            and_(Category.is_private, Topic.category_id.in_(category_ids)),
            Topic.author_id == user.id,
            Category.is_private == False,
            is_admin(user_id=user.id, db=db),
        )
    )

    if filter_params.order:
        order_by = asc if filter_params.order == "asc" else desc
        query = query.order_by(order_by(getattr(Topic, filter_params.order_by)))

    query = query.offset(filter_params.offset).limit(filter_params.limit).all()

    return query


def get_public(filter_params: TopicFilterParams, db: Session) -> list[Topic]:
    """
    Retrieve all public topics.

    Args:
        db (Session): The database session.
    Returns:
        list[Topic]: A list of public topics.
    """

    query = (
        db.query(Topic)
        .join(Category, Topic.category_id == Category.id)
        .filter(Category.is_private == False)
    )

    if filter_params.order:
        order_by = asc if filter_params.order == "asc" else desc
        query = query.order_by(order_by(getattr(Topic, filter_params.order_by)))

    query = query.offset(filter_params.offset).limit(filter_params.limit).all()

    return query


def get_by_id(topic_id: UUID, user: User, db: Session) -> Topic:
    """
    Retrieve a topic by its ID.

    Args:
        topic_id (UUID): The unique identifier of the topic.
        user (User): The user requesting the topic.
        db (Session): The database session.
    Returns:
        Topic: The topic object if found and accessible by the user.
    Raises:
        HTTPException: If the topic is not found or the user does not have permission to access it.
    """

    topic = db.query(Topic).filter(Topic.id == topic_id).first()
    if topic is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found"
        )

    if not is_admin(user_id=user.id, db=db):
        verify_topic_permission(topic=topic, user=user, db=db)

    return topic


def get_by_title(title: str, db: Session) -> Topic | None:
    """
    Retrieve a Topic from the database by its title.

    Args:
        title (str): The title of the topic to retrieve.
        db (Session): The database session to use for the query.

    Returns:
        Topic | None: The Topic object if found, otherwise None.
    """

    return db.query(Topic).filter(Topic.title == title).first()


def create(category_id: UUID, topic: TopicCreate, user: User, db: Session) -> Topic:
    """
    Create a new topic in the forum.

    Args:
        topic (TopicCreate): The topic data to be created.
        user (User): The user creating the topic.
        db (Session): The database session.
    Returns:
        Topic: The newly created topic.
    Raises:
        HTTPException: If the user does not have permission to create the topic.
        HTTPException: If a topic with the same title already exists.
    """

    if not user_permission(user=user, topic=topic, db=db, category_id=category_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to post in this category",
        )
    if get_by_title(title=topic.title, db=db) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Topic with this title already exists, please select a new title",
        )

    new_topic = Topic(
        author_id=user.id,
        category_id=category_id,
        is_locked=False,
        **topic.model_dump(),
    )
    db.add(new_topic)
    db.commit()
    db.refresh(new_topic)
    return new_topic


def update(
    user: User, topic_id: UUID, updated_topic: TopicUpdate, db: Session
) -> Topic:
    """
    Update a topic with new information provided by the user.

    Args:
        user (User): The user attempting to update the topic.
        topic_id (UUID): The unique identifier of the topic to be updated.
        updated_topic (TopicUpdate): An object containing the updated topic information.
        db (Session): The database session to use for the update.
    Returns:
        Topic: The updated topic object.
    Raises:
        HTTPException: If the user does not have permission to update the topic.
    """

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

    if updated_topic.content and updated_topic.content != topic.content:
        topic.content = updated_topic.content

    if any((updated_topic.title, updated_topic.category_id, updated_topic.content)):
        db.commit()
        db.refresh(topic)

    return topic


def get_replies(topic_id: UUID, db: Session) -> list[Reply]:
    """
    Retrieve all replies for a given topic.

    Args:
        topic_id (UUID): The unique identifier of the topic.
        db (Session): The database session used for querying.

    Returns:
        list[Reply]: A list of Reply objects associated with the given topic.
    """

    return (
        db.query(Reply)
        .options(joinedload(Reply.reactions))
        .filter(Reply.topic_id == topic_id)
        .all()
    )


def lock(user: User, topic_id: Topic, lock_topic: bool, db: Session) -> Topic:
    """
    Locks or unlocks a topic based on the provided parameters.

    Args:
        user (User): The user performing the action.
        topic_id (Topic): The ID of the topic to be locked or unlocked.
        lock_topic (bool): A boolean indicating whether to lock (True) or unlock (False) the topic.
        db (Session): The database session to use for the operation.

    Returns:
        Topic: The updated topic with the new lock status.
    """

    topic = get_by_id(topic_id=topic_id, user=user, db=db)
    topic.is_locked = lock_topic
    db.commit()
    db.refresh(topic)
    return topic


def select_best_reply(user: User, topic_id: UUID, reply_id: UUID, db: Session) -> Topic:
    """
    Selects the best reply for a given topic.

    Args:
        user (User): The user making the selection.
        topic_id (UUID): The ID of the topic.
        reply_id (UUID): The ID of the reply to be marked as the best.
        db (Session): The database session.
    Returns:
        Topic: The updated topic with the best reply set.
    """

    topic = _validate_topic_access(topic_id=topic_id, user=user, db=db)
    reply = get_reply_by_id(user=user, reply_id=reply_id, db=db)

    topic.best_reply_id = reply_id
    db.commit()
    db.refresh(topic)
    return topic


def get_topics_for_category(category_id: UUID, user: User, db: Session) -> list[Topic]:
    from forum_system_api.services.category_service import (
        get_by_id as get_category_by_id,
    )

    """
    Retrieve all topics for a given category.

    Args:
        category_id (UUID): The unique identifier of the category.
        user (User): The user requesting the topics.
        db (Session): The database session.
    Returns:
        list[Topic]: A list of topics that belong to the specified category.
    Raises:
        HTTPException: If the user is not authorized to access the category.
    """

    category = get_category_by_id(category_id=category_id, db=db)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )

    if (
        category.is_private
        and category.id not in (p.category_id for p in user.permissions)
        and not is_admin(user_id=user.id, db=db)
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized"
        )

    topics = db.query(Topic).filter(Topic.category_id == category_id).all()

    return topics


def _validate_topic_access(topic_id: UUID, user: User, db: Session) -> Topic:
    """
    Validates whether a user has access to a specific topic.

    Args:
        topic_id (UUID): The unique identifier of the topic.
        user (User): The user attempting to access the topic.
        db (Session): The database session.
    Returns:
        Topic: The topic if access is granted.
    Raises:
        HTTPException: If the user is not authorized to access the topic or if the topic is locked.
    """

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
