from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from forum_system_api.schemas.custom_types import MessageContent


class BaseMessage(BaseModel):
    content: MessageContent

    class Config:
        orm_mode = True


class MessageCreate(BaseMessage):
    receiver_id: UUID


class MessageResponse(BaseMessage):
    id: UUID
    author_id: UUID
    conversation_id: Optional[UUID]
    created_at: datetime
