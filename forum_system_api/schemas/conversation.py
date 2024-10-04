from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from ..schemas.message import MessageResponse


class BaseConversation(BaseModel):
    id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class ConversationResponse(BaseConversation):
    user1_id: UUID
    user2_id: UUID


class DetailedConversationResponse(BaseConversation):
    messages: list[MessageResponse]
    author_id: UUID
