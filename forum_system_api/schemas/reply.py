from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from forum_system_api.persistence.models.reply import Reply


class BaseReply(BaseModel):
    id: UUID
    content: str
    created_at: datetime
    topic_id: UUID
    author_id: UUID

    class Config:
        orm_mode = True


class ReplyCreate(BaseModel):
    content: str

    @field_validator("content")
    def validate_content(value):
        if 5 > len(value) <= 20:
            raise ValueError("Reply must be between 5-20 characters long")


class ReplyResponse(BaseReply):
    upvotes: int
    downvotes: int

    class Config:
        orm_mode = True

    @classmethod
    def create(cls, reply: Reply, votes: tuple):
        return cls(
            id=reply.id,
            content=reply.content,
            topic_id=reply.topic_id,
            author_id=reply.author_id,
            created_at=reply.created_at,
            upvotes=votes[0],
            downvotes=votes[1],
        )


class ReplyUpdate(BaseModel):
    content: Optional[str] = None

    class Config:
        orm_mode = True


class ReplyReactionCreate(BaseModel):
    reaction: Optional[bool] = None

    class Config:
        orm_mode = True


class ReplyReaction(BaseModel):
    reaction: bool
