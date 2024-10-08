from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import HTTPException

from forum_system_api.persistence.models.category import Category
from forum_system_api.schemas.category import CreateCategory, CategoryResponse


def create_category(data: CreateCategory, db: Session) -> CategoryResponse:
    new_category = Category(**data.model_dump())
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


def get_all(db: Session) -> list[CategoryResponse]:
    categories = db.query(Category).all()

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
    return (db.query(Category)
                .filter(Category.id == category_id)
                .one_or_none())


def make_private_or_public(
        category_id: UUID, 
        is_private: bool, 
        db: Session
) -> Category:
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
    category = get_by_id(category_id, db)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    category.is_locked = is_locked
    db.commit()
    db.refresh(category)

    return category
