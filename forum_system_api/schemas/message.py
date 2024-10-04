from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class MessageCreate(BaseModel):
    content: str
    conversation_id: UUID

    class Config:
        orm_mode = True


class MessageResponse(BaseModel):
    id: UUID
    content: str
    author_id: UUID
    conversation_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
