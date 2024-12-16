from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from forum_system_api.persistence.models.reply import Reply


class BaseReply(BaseModel):
    id: UUID
    content: str
    author: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    created_at: datetime
    topic_id: UUID
    author_id: UUID

    @field_validator("author", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        return value.strip()

    class Config:
        from_attributes = True


class ReplyCreate(BaseModel):
    content: str = Field(min_length=5, max_length=999, examples=["Example content"])


class ReplyResponse(BaseReply):
    upvotes: int
    downvotes: int

    class Config:
        from_attributes = True

    @classmethod
    def create(cls, reply: Reply, votes: tuple):
        return cls(
            id=reply.id,
            content=reply.content,
            author=reply.author.username,
            topic_id=reply.topic_id,
            author_id=reply.author_id,
            created_at=reply.created_at,
            upvotes=votes[0],
            downvotes=votes[1],
        )


class ReplyUpdate(BaseModel):
    content: Optional[str] = Field(default=None, examples=["Example content"])

    class Config:
        from_attributes = True


class ReplyReactionCreate(BaseModel):
    reaction: Optional[bool] = Field(default=None, examples=["True"])

    class Config:
        from_attributes = True
