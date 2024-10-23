from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.reply_reaction import ReplyReaction
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.reply import ReplyCreate, ReplyReactionCreate, ReplyUpdate
from forum_system_api.services.user_service import is_admin
from forum_system_api.services.utils.category_access_utils import (
    verify_topic_permission,
)


def get_by_id(user: User, reply_id: UUID, db: Session) -> Reply:
    from forum_system_api.services import topic_service

    reply = db.query(Reply).filter(Reply.id == reply_id).first()
    if reply is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Reply not found"
        )
    verify_topic_permission(
        topic=topic_service.get_by_id(topic_id=reply.topic_id, user=user, db=db),
        user=user,
        db=db,
    )

    return reply


def create(topic_id: UUID, reply: ReplyCreate, user: User, db: Session) -> Reply:
    topic = _validate_reply_access(topic_id=topic_id, user=user, db=db)
    verify_topic_permission(topic=topic, user=user, db=db)

    new_reply = Reply(topic_id=topic_id, author_id=user.id, **reply.model_dump())
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply


def update(
    user: User, reply_id: UUID, updated_reply: ReplyUpdate, db: Session
) -> Reply:
    existing_reply = get_by_id(user=user, reply_id=reply_id, db=db)
    topic = _validate_reply_access(topic_id=existing_reply.topic_id, user=user, db=db)
    verify_topic_permission(topic=topic, user=user, db=db)

    if user.id != existing_reply.author_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Cannot update reply"
        )

    if updated_reply.content:
        existing_reply.content = updated_reply.content
        db.commit()
        db.refresh(existing_reply)

    return existing_reply


def vote(
    reply_id: UUID, reaction: ReplyReactionCreate, user: User, db: Session
) -> Reply:
    reply = get_by_id(user=user, reply_id=reply_id, db=db)

    existing_vote = _get_vote_by_id(reply_id=reply_id, user_id=user.id, db=db)
    if existing_vote is None:
        return create_vote(user_id=user.id, reply=reply, reaction=reaction, db=db)

    if existing_vote.reaction != reaction.reaction:
        existing_vote.reaction = reaction.reaction
        db.commit()
    else:
        db.delete(existing_vote)
        db.commit()

    db.refresh(reply)
    return reply


def create_vote(
    user_id: UUID, reply: Reply, reaction: ReplyReactionCreate, db: Session
) -> Reply:
    user_vote = ReplyReaction(
        user_id=user_id, reply_id=reply.id, **reaction.model_dump()
    )
    db.add(user_vote)
    db.commit()
    db.refresh(reply)
    return reply


def _get_vote_by_id(reply_id: UUID, user_id: UUID, db: Session) -> ReplyReaction | None:
    existing_vote = (
        db.query(ReplyReaction).filter_by(user_id=user_id, reply_id=reply_id).first()
    )
    return existing_vote


def get_votes(reply: Reply):
    upvotes = sum(1 for reaction in reply.reactions if reaction.reaction)
    downvotes = sum(1 for reaction in reply.reactions if not reaction.reaction)
    return (upvotes, downvotes)


def _validate_reply_access(topic_id: UUID, user: User, db: Session) -> Topic:
    from forum_system_api.services.topic_service import get_by_id as get_topic_by_id

    topic = get_topic_by_id(topic_id=topic_id, user=user, db=db)
    if topic.is_locked and not is_admin(user_id=user.id, db=db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Topic is locked"
        )

    return topic
