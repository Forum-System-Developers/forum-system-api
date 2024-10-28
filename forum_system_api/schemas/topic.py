from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.schemas.custom_types import Title, TopicContent
from forum_system_api.schemas.reply import ReplyResponse


class BaseTopic(BaseModel):
    title: str
    content: str
    created_at: datetime
    id: UUID
    category_id: UUID
    best_reply_id: Optional[UUID]

    class Config:
        orm_mode = True


class TopicCreate(BaseModel):
    title: Title = Field(example="Example Title")
    content: TopicContent = Field(example="Example Content")
    category_id: UUID = Field(example="UUID")


class TopicResponse(BaseTopic):
    replies: list[ReplyResponse]

    class Config:
        orm_mode = True

    @classmethod
    def create(cls, topic: Topic, replies: list[Reply]):
        from forum_system_api.services.reply_service import get_votes

        return cls(
            title=topic.title,
            content=topic.content,
            created_at=topic.created_at,
            id=topic.id,
            category_id=topic.category_id,
            best_reply_id=topic.best_reply_id,
            replies=[
                ReplyResponse.create(reply=reply, votes=get_votes(reply=reply))
                for reply in replies
            ],
        )


class TopicUpdate(BaseModel):
    title: Optional[str] = Field(default=None, example="Example Title")
    content: Optional[str] = Field(default=None, example="Example Content")
    category_id: Optional[UUID] = Field(default=None, example="UUID")

    class Config:
        from_attributes = True
