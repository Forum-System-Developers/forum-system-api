import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forum_system_api.persistence.database import Base
from forum_system_api.persistence.models.access_level import AccessLevel

if TYPE_CHECKING:
    from forum_system_api.persistence.models.category import Category
    from forum_system_api.persistence.models.user import User


class UserCategoryPermission(Base):
    """
    Represents the permissions a user has for a specific category.

    Attributes:
        user_id (UUID): The unique identifier of the user. Foreign key referencing the users table.
        category_id (UUID): The unique identifier of the category. Foreign key referencing the categories table.
        access_level (AccessLevel): The level of access the user has to the category.
        user (User): The user associated with this permission.
        category (Category): The category associated with this permission.
    """

    __tablename__ = "user_category_permissions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True
    )
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=True
    )
    access_level: Mapped[AccessLevel] = mapped_column(Enum(AccessLevel), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="permissions")
    category: Mapped["Category"] = relationship(
        "Category", back_populates="permissions"
    )
