import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base

if TYPE_CHECKING:
    from forum_system_api.persistence.models.reply_reaction import ReplyReaction
    from forum_system_api.persistence.models.topic import Topic
    from forum_system_api.persistence.models.user import User


class Reply(Base):
    """
    Represents a reply in the forum system.

    Attributes:
        id (UUID): Unique identifier for the reply.
        content (str): The content of the reply.
        author_id (UUID): Foreign key referencing the user who authored the reply.
        topic_id (UUID): Foreign key referencing the topic to which the reply belongs.
        created_at (datetime): Timestamp when the reply was created.

    Relationships:
        author (User): The user who authored the reply.
        topic (Topic): The topic to which the reply belongs.
        reactions (list of ReplyReaction): The reactions associated with the reply.
    """

    __tablename__ = "replies"

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
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("topics.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    author: Mapped["User"] = relationship("User", back_populates="replies")
    topic: Mapped["Topic"] = relationship(
        "Topic", back_populates="replies", foreign_keys=[topic_id]
    )
    reactions: Mapped[List["ReplyReaction"]] = relationship(
        "ReplyReaction",
        back_populates="reply",
    )
