from sqlalchemy import Column, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from forum_system_api.persistence.database import Base


class CategoryPermission(Base):
    __tablename__ = "category_permissions"

    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    can_read = Column(Boolean, nullable=False)
    can_write = Column(Boolean, nullable=False)

    category = relationship("Category", back_populates="permissions")
    user = relationship("User", back_populates="permissions")
