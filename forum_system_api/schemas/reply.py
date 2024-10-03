from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class ReplyCreate(BaseModel):
    content: str
    
    
class ReplyResponse(BaseModel):
    content: str
    created_at: datetime
    topic_id: UUID
    author_id: UUID
    
    class Config:
        orm_mode = True

    
class ReplyUpdate(BaseModel):
    content: Optional[str]
    
    class Config:
        orm_mode = True