from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.reply_reaction import ReplyReaction
from forum_system_api.schemas.reply import ReplyCreate, ReplyUpdate, ReplyReactionCreate


def get_by_id(reply_id: UUID, db: Session) -> Reply:
    reply = (db.query(Reply)
            .filter(Reply.id == reply_id)
            .one_or_none())
    if reply is None:
        raise HTTPException(status_code=404)
       
    return reply


def create(topic_id: UUID, reply: ReplyCreate, user_id: UUID, db: Session) -> Reply:
    from forum_system_api.services.topic_service import get_by_id as get_topic_by_id

    topic = get_topic_by_id(topic_id=topic_id, db=db)
    if topic is None:
        raise HTTPException(status_code=404)
    if topic.is_locked:
        raise HTTPException(status_code=403, detail='Topic is locked.')
    
    new_reply = Reply(
        topic_id = topic_id,
        author_id = user_id,
        **reply.model_dump()
    )
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply


def update(user: User, reply_id: UUID, updated_reply: ReplyUpdate, db: Session) -> Reply:
    existing_reply = get_by_id(reply_id=reply_id, db=db)
    if user.id != existing_reply.author_id:
        raise HTTPException(status_code=403, detail='Unauthorized')
    
    if updated_reply.content:
        existing_reply.content = updated_reply.content
    
    db.commit()
    db.refresh(existing_reply)
    return existing_reply


def vote(reply_id: UUID, reaction: ReplyReactionCreate, user: User, db: Session) -> Reply:
    reply = get_by_id(reply_id=reply_id, db=db)
    if reply is None:
        raise HTTPException(status_code=404, detail='Reply could not be found')
    
    existing_vote = (db.query(ReplyReaction)
                     .filter_by(user_id=user.id, reply_id=reply_id)
                     .first())
    
    if existing_vote is None:
        return create_vote(user_id=user.id, reply=reply, reaction=reaction, db=db)
        
    if existing_vote.reaction != reaction.reaction:
        existing_vote.reaction = reaction.reaction 
        db.refresh(existing_vote)
    else:
        db.delete(existing_vote)

    db.commit()
    db.refresh(reply)
    return reply


def create_vote(user_id: UUID, reply: Reply, reaction: ReplyReactionCreate, db: Session) -> Reply:
    user_vote = ReplyReaction(
            user_id = user_id,
            reply_id = reply.id,
            **reaction.__dict__
        )
    db.add(user_vote)
    db.commit()
    db.refresh(user_vote)
    db.refresh(reply)
    return reply
    
    
def get_votes(reply: Reply):
    upvotes = sum(1 for reaction in reply.reactions if reaction.reaction)
    downvotes = sum(1 for reaction in reply.reactions if not reaction.reaction)
    return (upvotes, downvotes)
