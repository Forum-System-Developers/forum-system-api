from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from forum_system_api.schemas.common import FilterParams
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.services.topic_service import get_by_id as get_topic_by_id
from forum_system_api.schemas.reply import ReplyCreate, ReplyUpdate


def get_all(filter_params: FilterParams, db: Session) -> list[Reply]:
    query = db.query(Reply)
    
    if filter_params.order:
        if filter_params.order == 'asc':
            query = query.order_by(asc(getattr(Reply, filter_params.order_by)))
        else:
            query = query.order_by(desc(getattr(Reply, filter_params.order_by)))

    query = query.offset(filter_params.offset).limit(filter_params.limit)
    return query.all()


def get_by_id(reply_id: UUID, db: Session) -> Reply:
    reply = (db.query(Reply)
            .filter(Reply.id == reply_id)
            .one_or_none())
    if reply is None:
        raise HTTPException(status_code=404)
    
    return reply


def create(topic_id: UUID, reply: ReplyCreate, db: Session) -> Reply:
    topic = get_topic_by_id(topic_id=topic_id, db=db)
    if topic is None:
        raise HTTPException(status_code=404)
    
    new_reply = Reply(
        **reply.model_dump()
    )
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply


def update(reply_id: UUID, updated_reply: ReplyUpdate, db: Session) -> Reply:
    existing_reply = (db.query(Reply)
                      .filter(Reply.id == reply_id)
                      .one_or_none())
    if existing_reply is None:
        raise HTTPException(status_code=404)
    
    if updated_reply.content:
        existing_reply.content = updated_reply.content
    
    db.commit()
    db.refresh(existing_reply)
    return existing_reply
