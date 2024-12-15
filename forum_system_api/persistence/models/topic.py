import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base

if TYPE_CHECKING:
    from forum_system_api.persistence.models.category import Category
    from forum_system_api.persistence.models.reply import Reply
    from forum_system_api.persistence.models.user import User


class Topic(Base):
    """
    Represents a discussion topic in the forum system.

    Attributes:
        id (UUID): Unique identifier for the topic.
        title (str): Title of the topic.
        content (str): Content of the topic.
        is_locked (bool): Indicates if the topic is locked.
        created_at (datetime): Timestamp when the topic was created.
        author_id (UUID): Foreign key referencing the user who created the topic.
        category_id (UUID): Foreign key referencing the category of the topic.
        best_reply_id (UUID, optional): Foreign key referencing the best reply for the topic.

    Relationships:
        author (User): The user who created the topic.
        best_reply (Reply): The best reply for the topic.
        category (Category): The category to which the topic belongs.
        replies (list of Reply): The replies associated with the topic.
    """

    __tablename__ = "topics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    content: Mapped[str] = mapped_column(String(999), nullable=False)
    is_locked: Mapped[bool] = mapped_column(
        Boolean, server_default=text("false"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    author_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False
    )
    best_reply_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("replies.id"), nullable=True
    )

    author: Mapped["User"] = relationship("User", back_populates="topics")
    best_reply: Mapped["Reply"] = relationship("Reply", foreign_keys=[best_reply_id])
    category: Mapped["Category"] = relationship("Category", back_populates="topics")
    replies: Mapped[List["Reply"]] = relationship(
        "Reply",
        foreign_keys="Reply.topic_id",
        back_populates="topic",
    )
