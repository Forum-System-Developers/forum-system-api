from uuid import UUID
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseReply(BaseModel):
    content: str
    created_at: datetime
    topic_id: UUID
    author_id: UUID
    
    class Config:
        orm_mode = True
        

class ReplyCreate(BaseModel):
    content: str
    
    class Config:
        orm_mode = True
    
    
class ReplyResponse(BaseReply):
    pass

    
class ReplyUpdate(BaseModel):
    content: Optional[str]
    
    class Config:
        orm_mode = True