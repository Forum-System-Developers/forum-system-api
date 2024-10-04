from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseMessage(BaseModel):
    content: str
    conversation_id: Optional[UUID]

    class Config:
        orm_mode = True


class MessageCreate(BaseMessage):
    author_id: UUID
    receiver_id: UUID


class MessageResponse(BaseMessage):
    id: UUID
    author_id: UUID
    created_at: datetime