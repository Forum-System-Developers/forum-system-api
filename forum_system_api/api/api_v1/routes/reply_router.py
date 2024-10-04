from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from forum_system_api.schemas.common import FilterParams
from forum_system_api.schemas.reply import ReplyResponse, ReplyCreate, ReplyUpdate
from forum_system_api.persistence.database import get_db
from forum_system_api.services import reply_service


reply_router = APIRouter(prefix='/replies', tags=["replies"])


@reply_router.get('/', response_model=list[ReplyResponse], status_code=200)
def get_all(
    filter_query: FilterParams = Depends(),
    db: Session = Depends(get_db)
) -> list[ReplyResponse]:
    return reply_service.get_all(filter_params=filter_query, db=db)


@reply_router.get('/{reply_id}', response_model=ReplyResponse, status_code=200)
def get_by_id(
    reply_id: UUID,
    db: Session = Depends(get_db)
) -> ReplyResponse:
    reply = reply_service.get_by_id(reply_id=reply_id, db=db)
    if reply is None:
        raise HTTPException(status_code=404)
    return reply


@reply_router.post('/', response_model=ReplyResponse, status_code=201)
def create(
    topic_id: UUID,
    reply: ReplyCreate, 
    db: Session = Depends(get_db)
) -> ReplyResponse:
    reply = reply_service.create(topic_id=topic_id, reply=reply, db=db)
    if reply is None:
        raise HTTPException(status_code=404, detail='Topic not found')


@reply_router.put('/', response_model=ReplyResponse, status_code=201)
def update(
    reply_id: UUID, 
    updated_reply: ReplyUpdate, 
    db: Session = Depends(get_db)
) -> ReplyResponse:
    reply = reply_service.update(reply_id=reply_id, updated_reply=updated_reply, db=db)
    if not reply:
        raise HTTPException(status_code=404)
    return reply
