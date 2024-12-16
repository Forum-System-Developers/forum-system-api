import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List

from pydantic import EmailStr
from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base
from forum_system_api.persistence.models.conversation import Conversation

if TYPE_CHECKING:
    from forum_system_api.persistence.models.message import Message
    from forum_system_api.persistence.models.reply import Reply
    from forum_system_api.persistence.models.reply_reaction import ReplyReaction
    from forum_system_api.persistence.models.topic import Topic
    from forum_system_api.persistence.models.user_category_permission import (
        UserCategoryPermission,
    )


class User(Base):
    """
    Represents a user in the forum system.

    Attributes:
        id (UUID): Unique identifier for the user.
        username (str): Unique username for the user.
        password_hash (str): Hashed password for the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
        email (str): Unique email address of the user.
        created_at (datetime): Timestamp when the user was created.
        token_version (UUID): Unique token version for the user.

    Relationships:
        topics (list[Topic]): List of topics authored by the user.
        replies (list[Reply]): List of replies authored by the user.
        messages (list[Message]): List of messages authored by the user.
        permissions (list[UserCategoryPermission]): List of category permissions for the user.
        reactions (list[ReplyReaction]): List of reactions made by the user.
        conversations_as_user1 (list[Conversation]): List of conversations where the user is user1.
        conversations_as_user2 (list[Conversation]): List of conversations where the user is user2.

    Properties:
        conversations (list[Conversation]): Combined list of conversations where the user is either user1 or user2.

    Methods:
        __eq__(other): Checks equality between two User objects.
        __hash__(): Returns the hash of the user based on the id.
    """

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    token_version: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        server_default=func.uuid_generate_v4(),
        unique=True,
        nullable=False,
    )

    topics: Mapped[List["Topic"]] = relationship(
        "Topic",
        back_populates="author",
    )
    replies: Mapped[List["Reply"]] = relationship(
        "Reply",
        back_populates="author",
    )
    messages: Mapped[List["Message"]] = relationship(
        "Message",
        back_populates="author",
    )
    permissions: Mapped[List["UserCategoryPermission"]] = relationship(
        "UserCategoryPermission",
        back_populates="user",
    )
    reactions: Mapped[List["ReplyReaction"]] = relationship(
        "ReplyReaction",
        back_populates="user",
    )
    conversations_as_user1: Mapped[List["Conversation"]] = relationship(
        "Conversation",
        foreign_keys=[Conversation.user1_id],
        back_populates="user1",
    )
    conversations_as_user2: Mapped[List["Conversation"]] = relationship(
        "Conversation",
        foreign_keys=[Conversation.user2_id],
        back_populates="user2",
    )

    @property
    def conversations(self):
        return self.conversations_as_user1 + self.conversations_as_user2

    def __eq__(self, other) -> bool:
        if isinstance(other, User):
            return (
                self.id == other.id
                and self.username == other.username
                and self.password_hash == other.password_hash
                and self.email == other.email
                and self.first_name == other.first_name
                and self.last_name == other.last_name
                and self.token_version == other.token_version
                and self.created_at == other.created_at
            )
        return False

    def __hash__(self) -> int:
        return hash(self.id)
