from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from fastapi import HTTPException

from ..schemas.common import FilterParams
from ..persistence.models.reply import Reply
from ..schemas.reply import ReplyCreate, ReplyUpdate


def get_all(filter_params: FilterParams, db: Session) -> list[Reply]:
    query = (db.query(Reply)
             .offset(filter_params.offset)
             .limit(filter_params.limit))
    
    if filter_params.order == 'asc':
        query = query.order_by(asc(getattr(Reply, filter_params.order_by)))
    else:
        query = query.order_by(desc(getattr(Reply, filter_params.order_by)))

    replies = query.all()
    return replies


def get_by_id(reply_id: UUID, db: Session) -> Reply:
    return (db.query(Reply)
            .filter(Reply.id == reply_id)
            .first())


def create(reply: ReplyCreate, db: Session) -> Reply:
    new_reply = reply(content = reply.content)
    db.add(new_reply)
    db.commit()
    db.refresh(new_reply)
    return new_reply


def update(reply_id: UUID, updated_reply: ReplyUpdate, db: Session) -> Reply:
    existing_reply = (db.query(Reply)
                      .filter(Reply.id == reply_id)
                      .first())
    
    if not existing_reply:
        raise HTTPException(status_code=404)
    
    if updated_reply.content:
        existing_reply.content = updated_reply.content
    
    db.commit()
    db.refresh(existing_reply)
    return existing_reply


def delete(reply_id: UUID, db: Session) -> None:
    reply = (db.query(Reply)
             .filter(Reply.id == reply_id)
             .first())
    
    if not reply:
        raise HTTPException(status_code=404)
    
    db.delete(reply)
    db.commit()