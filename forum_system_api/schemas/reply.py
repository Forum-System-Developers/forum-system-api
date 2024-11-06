from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.schemas.custom_types import Content, Username


class BaseReply(BaseModel):
    id: UUID
    content: str
    author: Username
    created_at: datetime
    topic_id: UUID
    author_id: UUID

    class Config:
        from_attributes = True


class ReplyCreate(BaseModel):
    content: Content = Field(example="Example content")


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
    content: Optional[str] = Field(default=None, example="Example content")

    class Config:
        from_attributes = True


class ReplyReactionCreate(BaseModel):
    reaction: Optional[bool] = Field(default=None, example="True")

    class Config:
        from_attributes = True
