import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.database import Base


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

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)
    title = Column(String(255), unique=True, nullable=False)
    content = Column(String(999), nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    best_reply_id = Column(UUID(as_uuid=True), ForeignKey("replies.id"), default=None, nullable=True)

    author = relationship("User", back_populates="topics")
    best_reply = relationship("Reply", foreign_keys=[best_reply_id])
    category = relationship("Category", back_populates="topics")
    replies = relationship("Reply", foreign_keys=[Reply.topic_id], back_populates="topic")
