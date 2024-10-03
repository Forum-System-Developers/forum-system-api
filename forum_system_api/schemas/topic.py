from pydantic import BaseModel
# from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID  
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
    
    # class Config:
    #     model_config = {
    #         'from_attributes': True
    #     }

    @classmethod
    def from_orm(cls, obj):
        return cls(**obj.__dict__)

class CreateTopic(BaseModel):
    title: str
    is_locked: Optional[bool] = False
    author_id: UUID
    category_id: UUID
    
    
class TopicResponse(BaseModel):
    # from .reply import Reply
    # from .category_schema import Category

    title: str
    created_at: date
    author_id: UUID
    category_id: UUID
    # replies: list[Reply]
    best_reply: Optional[UUID]
    
    # class Config:
    #     model_config = {
    #         'from_attributes': True
    #     }
    @classmethod
    def from_orm(cls, obj):
        return cls(**obj.__dict__)

    
class TopicUpdate(BaseModel):
    title: Optional[str]
    is_locked: Optional[bool]
    category: Optional[UUID]
    best_reply: Optional[UUID]

    @classmethod
    def from_orm(cls, obj):
        return cls(**obj.__dict__)

