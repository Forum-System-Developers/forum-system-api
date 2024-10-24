import uuid
from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from forum_system_api.persistence.database import Base


class Conversation(Base):
    """
    Represents a conversation between two users.

    Attributes:
        id (UUID): Unique identifier for the conversation.
        created_at (DateTime): Timestamp when the conversation was created.
        user1_id (UUID): Foreign key referencing the first user in the conversation.
        user2_id (UUID): Foreign key referencing the second user in the conversation.
        user1 (User): Relationship to the first user in the conversation.
        user2 (User): Relationship to the second user in the conversation.
        messages (list of Message): List of messages in the conversation.
    """
    __tablename__ = "conversations"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user1_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user2_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    user1 = relationship("User", foreign_keys=[user1_id], back_populates="conversations_as_user1")
    user2 = relationship("User", foreign_keys=[user2_id], back_populates="conversations_as_user2")
    messages = relationship("Message", back_populates="conversation")
