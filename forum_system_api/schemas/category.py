from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    is_private: bool
    is_locked: bool

    class Config:
        orm_mode = True


class CreateCategory(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime
    topic_count: int = 0
