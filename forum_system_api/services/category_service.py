import logging
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.category import Category
from forum_system_api.schemas.category import CategoryResponse, CreateCategory

logger = logging.getLogger(__name__)


def create_category(data: CreateCategory, db: Session) -> CategoryResponse:
    """
    Creates a new category in the database.

    Args:
        data (CreateCategory): The data required to create a new category.
        db (Session): The database session used to interact with the database.
    Returns:
        CategoryResponse: The newly created category.
    """
    new_category = Category(**data.model_dump())

    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    logger.info(f"Created a new category with ID: {new_category.id}")

    return CategoryResponse.model_validate(new_category, from_attributes=True)


def get_all(db: Session) -> list[CategoryResponse]:
    """
    Retrieve all categories from the database.

    Args:
        db (Session): The database session.
    Returns:
        list[CategoryResponse]: A list of CategoryResponse objects representing all categories.
    Raises:
        HTTPException: If no categories are found in the database.
    """
    categories = db.query(Category).all()

    if not categories:
        logger.error("No categories found in the database")
        raise HTTPException(status_code=404, detail="There are no categories yet")

    logger.info("Retrieved all categories from the database")

    result = [
        CategoryResponse(
            id=category.id,
            name=category.name,
            is_private=category.is_private,
            is_locked=category.is_locked,
            created_at=category.created_at,
            topic_count=len(category.topics),
        )
        for category in categories
    ]
    logger.info("Converted categories to CategoryResponse objects")

    return result


def get_by_id(category_id: UUID, db: Session) -> Category | None:
    """
    Retrieve a category by its ID.

    Args:
        category_id (UUID): The unique identifier of the category.
        db (Session): The database session used for querying.

    Returns:
        Category: The category object if found, otherwise None.
    """
    category = db.query(Category).filter(Category.id == category_id).first()
    logger.warning(
        f"Retrieved category with ID: {category_id} from the database if it exists or None otherwise"
    )

    return category


def make_private_or_public(
    category_id: UUID, is_private: bool, db: Session
) -> Category:
    """
    Update the privacy status of a category.

    Args:
        category_id (UUID): The unique identifier of the category.
        is_private (bool): The desired privacy status of the category.
        db (Session): The database session to use for the operation.
    Returns:
        Category: The updated category object.
    Raises:
        HTTPException: If the category with the given ID is not found.
    """
    category = get_by_id(category_id, db)

    if category is None:
        logger.error(f"Category with ID {category_id} not found")
        raise HTTPException(status_code=404, detail="Category not found")
    logger.info(f"Get category by ID: {category_id}")

    category.is_private = is_private
    db.commit()
    db.refresh(category)
    logger.info(f"Updated category with ID: {category_id}")

    return category


def lock_or_unlock(category_id: UUID, is_locked: bool, db: Session) -> Category:
    """
    Lock or unlock a category based on the provided category ID.

    Args:
        category_id (UUID): The unique identifier of the category to be locked or unlocked.
        is_locked (bool): A boolean indicating whether to lock (True) or unlock (False) the category.
        db (Session): The database session used to perform the operation.
    Returns:
        Category: The updated category object.
    Raises:
        HTTPException: If the category with the given ID is not found.
    """
    category = get_by_id(category_id, db)

    if category is None:
        logger.error(f"Category with ID {category_id} not found")
        raise HTTPException(status_code=404, detail="Category not found")
    logger.info(f"Get category by ID: {category_id}")

    category.is_locked = is_locked
    db.commit()
    db.refresh(category)
    logger.info(f"Updated category with ID: {category_id}")

    return category
