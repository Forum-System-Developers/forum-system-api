from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import UUID
from datetime import date, datetime
from typing import Optional
# from .user_schema import User


class Topic(BaseModel):
    id: UUID
    title: str
    is_locked: bool
    created_at: date
    author_id: UUID
    category_id: UUID
    replies: list[UUID]
    best_reply: Optional[UUID]
    
    class Config:
        model_config = {
            'from_attributes': True
        }


class CreateTopic(BaseModel):
    id: Optional[UUID]
    title: str
    is_locked: Optional[bool] = False
    created_at: date
    author: UUID
    category: UUID
    
    
class TopicResponse(BaseModel):
    from .reply import Reply
    # from .category_schema import Category

    title: str
    created_at: date
    author: UUID ## to be changed back when category and user are created
    category: UUID
    replies: list[Reply]
    best_reply: Optional[UUID]
    
    class Config:
        model_config = {
            'from_attributes': True
        }


    
class TopicUpdate(BaseModel):
    title: Optional[str] = None
    is_locked: Optional[bool] = None
    category: Optional[UUID] = None
    best_reply: Optional[UUID] = None
    
    class Config:
        model_config = {
            'from_attributes': True
        }

