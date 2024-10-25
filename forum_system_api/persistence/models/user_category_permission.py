from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from forum_system_api.persistence.database import Base
from forum_system_api.persistence.models.access_level import AccessLevel


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

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=True)
    access_level = Column(Enum(AccessLevel), nullable=False)

    user = relationship("User", back_populates="permissions")
    category = relationship("Category", back_populates="permissions")
