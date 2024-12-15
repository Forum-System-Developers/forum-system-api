import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base

if TYPE_CHECKING:
    from forum_system_api.persistence.models.topic import Topic
    from forum_system_api.persistence.models.user_category_permission import (
        UserCategoryPermission,
    )


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

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    is_private: Mapped[bool] = mapped_column(
        Boolean, server_default=text("false"), nullable=False
    )
    is_locked: Mapped[bool] = mapped_column(
        Boolean, server_default=text("false"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    permissions: Mapped[list["UserCategoryPermission"]] = relationship(
        "UserCategoryPermission",
        back_populates="category",
        uselist=True,
        collection_class=list,
    )
    topics: Mapped[list["Topic"]] = relationship(
        "Topic", back_populates="category", uselist=True, collection_class=list
    )
