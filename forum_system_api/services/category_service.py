from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.category import Category


def get_by_id(category_id: UUID, db: Session) -> Category:
    category = (db.query(Category)
                .filter(Category.id == category_id)
                .one_or_none())
    
    if category is None:
        raise HTTPException(status_code=404, detail='Category not found')