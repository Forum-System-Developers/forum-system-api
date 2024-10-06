from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func


from forum_system_api.persistence.models.category import Category
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.schemas.category import CreateCategory, CategoryResponse



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
    category = (db.query(Category)
                .filter(Category.id == category_id)
                .one_or_none())
    
    if category is None:
        raise HTTPException(status_code=404, detail='Category not found')
    
    return category
    

def create_category(data: CreateCategory, db: Session) -> Category:
    new_category = Category(
        **data.model_dump()
        )
   
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
 
    return new_category

 