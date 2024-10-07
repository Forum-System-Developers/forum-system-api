from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class BaseMessage(BaseModel):
    content: str

    class Config:
        orm_mode = True


class MessageCreate(BaseMessage):
    receiver_id: UUID


class MessageResponse(BaseMessage):
    id: UUID
    author_id: UUID
    conversation_id: Optional[UUID]
    created_at: datetime