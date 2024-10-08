import uuid
from sqlalchemy import Column, DateTime, String, or_
from sqlalchemy.dialects.postgresql import UUID
from forum_system_api.persistence.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from forum_system_api.persistence.models.conversation import Conversation


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(64), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    token_version = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)

    topics = relationship("Topic", back_populates="author")
    replies = relationship("Reply", back_populates="author")
    messages = relationship("Message", back_populates="author")
    permissions = relationship("UserCategoryPermission", back_populates="user")
    reactions = relationship("ReplyReaction", back_populates="user")
    conversations_as_user1 = relationship("Conversation", foreign_keys=[Conversation.user1_id], back_populates="user1")
    conversations_as_user2 = relationship("Conversation", foreign_keys=[Conversation.user2_id], back_populates="user2")

    @property
    def conversations(self):
        return self.conversations_as_user1 + self.conversations_as_user2
