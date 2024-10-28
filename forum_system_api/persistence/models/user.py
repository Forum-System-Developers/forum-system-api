from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from forum_system_api.persistence.database import Base
from forum_system_api.persistence.models.conversation import Conversation


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

    id = Column(UUID(as_uuid=True), server_default=func.uuid_generate_v4(), primary_key=True, unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(64), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    token_version = Column(UUID(as_uuid=True), server_default=func.uuid_generate_v4(), unique=True, nullable=False)

    topics = relationship("Topic", back_populates="author")
    replies = relationship("Reply", back_populates="author")
    messages = relationship("Message", back_populates="author")
    permissions = relationship("UserCategoryPermission", back_populates="user")
    reactions = relationship("ReplyReaction", back_populates="user")
    conversations_as_user1 = relationship("Conversation", foreign_keys=[Conversation.user1_id], back_populates="user1")
    conversations_as_user2 = relationship("Conversation", foreign_keys=[Conversation.user2_id], back_populates="user2")

    @property
    def conversations(self):
        return self.conversations_as_user1 + self.conversations_as_user2

    def __eq__(self, other) -> bool:
        if isinstance(other, User):
            return (
                self.id == other.id and
                self.username == other.username and
                self.password_hash == other.password_hash and
                self.email == other.email and
                self.first_name == other.first_name and
                self.last_name == other.last_name and
                self.token_version == other.token_version and
                self.created_at == other.created_at
            )
        return False

    def __hash__(self) -> int:
        return hash(self.id)
