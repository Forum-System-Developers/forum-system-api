from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.schemas.custom_types import Content


class BaseReply(BaseModel):
    id: UUID
    content: str
    created_at: datetime
    topic_id: UUID
    author_id: UUID

    class Config:
        orm_mode = True


class ReplyCreate(BaseModel):
    content: Content = Field(example="Example content")


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
    content: Optional[str] = Field(default=None, example="Example content")

    class Config:
        orm_mode = True


class ReplyReactionCreate(BaseModel):
    reaction: Optional[bool] = Field(default=None, example="True")

    class Config:
        orm_mode = True
