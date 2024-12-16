import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forum_system_api.persistence.database import Base

if TYPE_CHECKING:
    from forum_system_api.persistence.models.reply import Reply
    from forum_system_api.persistence.models.user import User


class ReplyReaction(Base):
    """
    Represents a reaction to a reply in the forum system.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        user_id (UUID): The ID of the user who reacted to the reply. This is a primary key and a foreign key referencing the users table.
        reply_id (UUID): The ID of the reply that was reacted to. This is a primary key and a foreign key referencing the replies table.
        reaction (bool): The type of reaction (e.g., like or dislike). This field is not nullable.
        created_at (DateTime): The timestamp when the reaction was created. This field is not nullable and defaults to the current time.

    Relationships:
        user (User): The user who reacted to the reply.
        reply (Reply): The reply that was reacted to.
    """

    __tablename__ = "reply_reactions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )
    reply_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("replies.id"), primary_key=True
    )
    reaction: Mapped[bool] = mapped_column(Boolean, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="reactions")
    reply: Mapped["Reply"] = relationship("Reply", back_populates="reactions")
