from sqlalchemy import Boolean, Column, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from forum_system_api.persistence.database import Base


class ReplyReaction(Base):
    __tablename__ = 'reply_reactions'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    reply_id = Column(UUID(as_uuid=True), ForeignKey("replies.id"), primary_key=True)
    reaction = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="reactions")
    reply = relationship("Reply", back_populates="reactions")
