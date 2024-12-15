from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class BaseMessage(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=10_000,
        examples=["Example content"],
    )

    class Config:
        from_attributes = True


class MessageCreate(BaseMessage):
    receiver_id: UUID


class MessageCreateByUsername(BaseMessage):
    receiver_username: str = Field(
        min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$"
    )

    @field_validator("receiver_username", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        return value.strip()


class MessageResponse(BaseMessage):
    id: UUID
    author_id: UUID
    conversation_id: Optional[UUID]
    created_at: datetime
