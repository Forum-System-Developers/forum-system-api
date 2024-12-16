import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forum_system_api.persistence.database import Base

if TYPE_CHECKING:
    from forum_system_api.persistence.models.message import Message
    from forum_system_api.persistence.models.user import User


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

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    user1_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    user2_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )

    user1: Mapped["User"] = relationship(
        "User", foreign_keys=[user1_id], back_populates="conversations_as_user1"
    )
    user2: Mapped["User"] = relationship(
        "User", foreign_keys=[user2_id], back_populates="conversations_as_user2"
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="conversation",
    )
