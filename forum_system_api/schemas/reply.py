from pydantic import BaseModel
# from sqlalchemy.dialects.postgresql import UUID
from uuid import UUID  
from datetime import date, datetime
from typing import Optional


class Reply(BaseModel):
    id: UUID
    content: str
    created_at: date
    author_id: UUID
    topic_id: UUID
    
    class Config:
        orm_mode = True


class CreateReply(BaseModel):
    content: str
    
    
class ReplyResponse(BaseModel):
    content: str
    created_at: date
    topic_id: UUID
    author_id: UUID
    
    class Config:
        orm_mode = True


    
class ReplyUpdate(BaseModel):
    content: Optional[str]
    
    class Config:
        orm_mode = True