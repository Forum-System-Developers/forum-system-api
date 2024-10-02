import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base

class Topic(Base):
    __tablename__ = "topics"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)
    title = Column(String(255), nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    best_reply_id = Column(UUID(as_uuid=True), ForeignKey("replies.id"), default=None, nullable=True)

    author = relationship("User", back_populates="topics")
    best_reply = relationship("Reply", foreign_keys=[best_reply_id])
    category = relationship("Category", back_populates="topics")
    replies = relationship("Reply", back_populates="topic")
