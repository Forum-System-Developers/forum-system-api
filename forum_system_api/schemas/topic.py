from datetime import datetime
from uuid import UUID  
from typing import Optional

from pydantic import BaseModel

from .reply import ReplyResponse
# from .user_schema import User


class BaseTopic(BaseModel):
    title: str
    created_at: datetime
    author_id: UUID
    category_id: UUID
    replies: list[ReplyResponse]
    best_reply: Optional[UUID]
    

class TopicCreate(BaseModel):
    title: str
    category_id: UUID
    
    
class TopicResponse(BaseTopic):
    pass

   
class TopicUpdate(BaseModel):
    title: Optional[str]
    is_locked: Optional[bool]
    category: Optional[UUID]
    best_reply: Optional[UUID]

    class Config:
        orm_mode = True

