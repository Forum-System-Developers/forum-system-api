from pydantic import BaseModel
# from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID  
from datetime import date, datetime
from typing import Optional
# from .user_schema import User
# from .category_schema import Category


class Reply(BaseModel):
    id: UUID
    content: str
    author_id: UUID
    topic_id: UUID
    created_at: date
    
    class Config:
        model_config = {
            'from_attributes': True
        }



class CreateReply(BaseModel):
    content: str
    author_id: UUID
    topic_id: UUID
    
    
class ReplyResponse(BaseModel):
    title: str
    created_at: date
    topic_id: UUID
    author_id: UUID
    
    class Config:
        model_config = {
            'from_attributes': True
        }


    
class ReplyUpdate(BaseModel):
    title: Optional[str]
    is_locked: Optional[bool]
    category: Optional[UUID]
    best_reply: Optional[UUID]
    
    class Config:
        model_config = {
            'from_attributes': True
        }

