import uuid
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    is_private = Column(Boolean, default=False, nullable=False)
    is_locked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    permissions = relationship("UserCategoryPermission", back_populates="category")
    topics = relationship("Topic", back_populates="category")
