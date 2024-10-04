from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class CategoryBase(BaseModel):
    name: str
    is_private: bool = False
    is_locked: bool = False

class CreateCategory(CategoryBase):
    created_at: datetime

class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
