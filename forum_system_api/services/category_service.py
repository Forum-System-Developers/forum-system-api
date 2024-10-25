from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException

from forum_system_api.persistence.models.category import Category
from forum_system_api.schemas.category import CreateCategory, CategoryResponse


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

    return new_category


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
        raise HTTPException(status_code=404, detail="There are no categories yet")

    result = [
            CategoryResponse(
                id=category.id,
                name=category.name,
                is_private=category.is_private,
                is_locked=category.is_locked,
                created_at=category.created_at,
                topic_count=len(category.topics)
            )
            for category in categories
        ]

    return result


def get_by_id(category_id: UUID, db: Session) -> Category:
    """
    Retrieve a category by its ID.

    Args:
        category_id (UUID): The unique identifier of the category.
        db (Session): The database session used for querying.

    Returns:
        Category: The category object if found, otherwise None.
    """
    return (db.query(Category)
                .filter(Category.id == category_id)
                .first())


def make_private_or_public(
        category_id: UUID, 
        is_private: bool, 
        db: Session
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
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.is_private = is_private
    db.commit()
    db.refresh(category)

    return category


def lock_or_unlock(
        category_id: UUID, 
        is_locked: bool, 
        db: Session
) -> Category:
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
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.is_locked = is_locked
    db.commit()
    db.refresh(category)

    return category
