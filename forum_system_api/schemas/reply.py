from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from datetime import date, datetime
from typing import Optional
from .user_schema import User
from .category_schema import Category


class Reply(BaseModel):
    id: UUID
    content: str
    author_id: UUID
    topic_id: UUID
    created_at: date


class CreateReply(BaseModel):
    content: str
    author_id: UUID
    topic_id: UUID
    created_at: date
    
    
class ReplyResponse(BaseModel):
    title: str
    created_at: date
    author_id: UUID
    category: Category
    replies: list[Reply]
    best_reply: Optional[UUID]
    
    
class ReplyUpdate(BaseModel):
    title: Optional[str]
    is_locked: Optional[bool]
    category: Optional[UUID]
    best_reply: Optional[UUID]