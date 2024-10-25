import uuid
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base


class Category(Base):
    """
    Represents a category in the forum system.

    Attributes:
        id (UUID): Unique identifier for the category.
        name (str): Name of the category, must be unique.
        is_private (bool): Indicates if the category is private.
        is_locked (bool): Indicates if the category is locked.
        created_at (datetime): Timestamp when the category was created.
        permissions (relationship): Relationship to UserCategoryPermission, defining permissions for the category.
        topics (relationship): Relationship to Topic, containing topics under the category.
    """
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    is_private = Column(Boolean, default=False, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    permissions = relationship("UserCategoryPermission", back_populates="category")
    topics = relationship("Topic", back_populates="category")
