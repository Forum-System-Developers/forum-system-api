import uuid
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base


class Admin(Base):
    """
    Admin model representing the admin table in the database.

    Attributes:
        id (UUID): Unique identifier for the admin. Defaults to a new UUID.
        created_at (DateTime): Timestamp when the admin record was created. Defaults to the current time.
        user_id (UUID): Foreign key referencing the user associated with the admin. Must be unique and not nullable.

    Relationships:
        user (User): Relationship to the User model, linked by the user_id foreign key.
    """
    __tablename__ = "admins"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    