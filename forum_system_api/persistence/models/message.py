import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base

if TYPE_CHECKING:
    from forum_system_api.persistence.models.conversation import Conversation
    from forum_system_api.persistence.models.user import User


class Message(Base):
    """
    Represents a message in the forum system.

    Attributes:
        id (UUID): Unique identifier for the message.
        content (str): The content of the message.
        author_id (UUID): Foreign key referencing the user who authored the message.
        conversation_id (UUID): Foreign key referencing the conversation to which the message belongs.
        created_at (datetime): Timestamp when the message was created.

    Relationships:
        author (User): The user who authored the message.
        conversation (Conversation): The conversation to which the message belongs.
    """

    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    content: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    author: Mapped["User"] = relationship("User", back_populates="messages")
    conversation: Mapped["Conversation"] = relationship(
        "Conversation", back_populates="messages"
    )
