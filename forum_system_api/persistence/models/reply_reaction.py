from sqlalchemy import Boolean, Column, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from forum_system_api.persistence.database import Base


class ReplyReaction(Base):
    """
    Represents a reaction to a reply in the forum system.
    
    Attributes:
        __tablename__ (str): The name of the table in the database.
        user_id (UUID): The ID of the user who reacted to the reply. This is a primary key and a foreign key referencing the users table.
        reply_id (UUID): The ID of the reply that was reacted to. This is a primary key and a foreign key referencing the replies table.
        reaction (bool): The type of reaction (e.g., like or dislike). This field is not nullable.
        created_at (DateTime): The timestamp when the reaction was created. This field is not nullable and defaults to the current time.
    
    Relationships:
        user (User): The user who reacted to the reply.
        reply (Reply): The reply that was reacted to.
    """
    __tablename__ = "reply_reactions"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), primary_key=True)
    reply_id = Column(UUID(as_uuid=True), ForeignKey("replies.id"), primary_key=True)
    reaction = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="reactions")
    reply = relationship("Reply", back_populates="reactions")
