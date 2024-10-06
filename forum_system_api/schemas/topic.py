from datetime import datetime
from uuid import UUID  
from typing import Optional

from pydantic import BaseModel

from .reply import BaseReply
# from .user_schema import User


class BaseTopic(BaseModel):
    title: str
    created_at: datetime
    id: UUID
    category_id: UUID
    best_reply_id: Optional[UUID]
    replies: list[BaseReply]
    

class TopicCreate(BaseModel):
    title: str
    category_id: UUID
    
    
class TopicResponse(BaseTopic):
    pass

   
class TopicUpdate(BaseModel):
    title: Optional[str]
    is_locked: Optional[bool] = False
    category_id: Optional[UUID]
    best_reply_id: Optional[UUID]

    class Config:
        orm_mode = True
