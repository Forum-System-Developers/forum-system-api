from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from forum_system_api.persistence.database import Base
from forum_system_api.persistence.models.access_level import AccessLevel


class UserCategoryPermission(Base):
    __tablename__ = "user_category_permissions"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=True)
    access_level = Column(Enum(AccessLevel), nullable=False)

    user = relationship("User", back_populates="permissions")
    category = relationship("Category", back_populates="permissions")
