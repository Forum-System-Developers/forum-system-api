from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from forum_system_api.schemas.custom_types import Title_for_category


class CategoryBase(BaseModel):
    name: Title_for_category
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
