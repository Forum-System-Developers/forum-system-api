from pydantic import BaseModel
from uuid import UUID  
from datetime import date
from typing import Optional
# from .user_schema import User


class TopicCreate(BaseModel):
    title: str
    # is_locked: Optional[bool] = False
    # author_id: UUID
    # category_id: UUID
    
    
class TopicResponse(BaseModel):
    # from .reply import Reply
    # from .category_schema import Category

    title: str
    created_at: date
    author_id: UUID
    category_id: UUID
    # replies: list[Reply]
    best_reply: Optional[UUID]
    
    class Config:
        orm_mode = True

    
class TopicUpdate(BaseModel):
    title: Optional[str]
    is_locked: Optional[bool]
    category: Optional[UUID]
    best_reply: Optional[UUID]

    class Config:
        orm_mode = True

