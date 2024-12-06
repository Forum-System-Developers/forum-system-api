from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from forum_system_api.schemas.custom_types import MessageContent, Username


class BaseMessage(BaseModel):
    content: MessageContent

    class Config:
        from_attributes = True


class MessageCreate(BaseMessage):
    receiver_id: UUID


class MessageCreateByUsername(BaseMessage):
    receiver_username: Username


class MessageResponse(BaseMessage):
    id: UUID
    author_id: UUID
    conversation_id: Optional[UUID]
    created_at: datetime
