from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.schemas.reply import ReplyResponse


class BaseTopic(BaseModel):
    title: str
    content: str
    author: str = Field(min_length=3, max_length=30, pattern=r"^[a-zA-Z0-9_]+$")
    created_at: datetime
    id: UUID
    category_id: UUID
    best_reply_id: Optional[UUID]

    @field_validator("author", mode="before")
    def strip_whitespace(cls, value: str) -> str:
        return value.strip()

    class Config:
        from_attributes = True


class TopicCreate(BaseModel):
    title: str = Field(min_length=5, max_length=50, examples=["Example Title"])
    content: str = Field(min_length=5, max_length=999, examples=["Example Content"])


class TopicResponse(BaseTopic):
    author_id: UUID
    is_locked: bool
    replies: list[ReplyResponse]

    class Config:
        from_attributes = True

    @classmethod
    def create(cls, topic: Topic, replies: list[Reply]):
        from forum_system_api.services.reply_service import get_votes

        return cls(
            title=topic.title,
            content=topic.content,
            author=topic.author.username,
            author_id=topic.author.id,
            created_at=topic.created_at,
            id=topic.id,
            category_id=topic.category_id,
            best_reply_id=topic.best_reply_id,
            is_locked=topic.is_locked,
            replies=[
                ReplyResponse.create(reply=reply, votes=get_votes(reply=reply))
                for reply in replies
            ],
        )


class TopicUpdate(BaseModel):
    title: str | None = Field(examples=["Example Title"])
    content: str | None = Field(examples=["Example Content"])
    category_id: UUID | None = Field(examples=["UUID"])

    class Config:
        from_attributes = True
