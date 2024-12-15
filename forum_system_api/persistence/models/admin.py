import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base

if TYPE_CHECKING:
    from forum_system_api.persistence.models.user import User


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

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), unique=True, nullable=False
    )

    user: Mapped["User"] = relationship("User", foreign_keys=[user_id])
