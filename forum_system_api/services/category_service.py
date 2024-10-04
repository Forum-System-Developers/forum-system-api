from uuid import UUID

from sqlalchemy.orm import Session

from ..persistence.models.category import Category


def get_by_id(category_id: UUID, db: Session) -> Category:
    return (db.query(Category)
                .filter(Category.id == category_id)
                .one_or_none())