from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class ConversationResponse(BaseModel):
    id: UUID
    user1_id: UUID
    user2_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationMessagesResponse(BaseModel):
    id: UUID
    content: str
    author_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
