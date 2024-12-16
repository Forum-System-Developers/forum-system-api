from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CategoryBase(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=30,
        pattern=r"^[a-zA-Z0-9 ]+$",
        examples=["Example Category Name"],
    )
    is_private: bool
    is_locked: bool

    class Config:
        from_attributes = True

    @field_validator("name", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        return value.strip()


class CreateCategory(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: UUID
    created_at: datetime
    topic_count: int = 0
