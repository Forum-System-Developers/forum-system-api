import uuid
from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from forum_system_api.persistence.database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user1_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user2_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    participants = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")
