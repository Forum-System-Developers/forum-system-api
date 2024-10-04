from fastapi import APIRouter
from fastapi import Depends
from ....schemas.common import FilterParams
from ....schemas.reply import ReplyResponse, ReplyCreate, ReplyUpdate
from ....persistence.database import get_db
from sqlalchemy.orm import Session
from uuid import UUID
from ....services import reply_service

reply_router = APIRouter(prefix='/replies', tags=["replies"])



@reply_router.get('/', response_model=list[ReplyResponse], status_code=200)
def get_all(
    filter_query: FilterParams = Depends(),
    db: Session = Depends(get_db)
):
    return reply_service.get_all(filter_params=filter_query, db=db)


@reply_router.get('/{reply_id}', response_model=ReplyResponse, status_code=200)
def get_by_id(
    reply_id: UUID,
    db: Session = Depends(get_db)
):
    return reply_service.get_by_id(reply_id=reply_id, db=db)


@reply_router.post('/', response_model=ReplyResponse, status_code=201)
def create(
    reply: ReplyCreate, 
    db: Session = Depends(get_db)
):
    return reply_service.create_reply(reply=reply, db=db)


@reply_router.put('/', response_model=ReplyResponse, status_code=200)
def update(
    reply_id: UUID, 
    updated_reply: ReplyUpdate, 
    db: Session = Depends(get_db)
):
    return reply_service.update_reply(reply_id=reply_id, updated_reply=updated_reply, db=db)


@reply_router.delete('/', status_code=204)
def delete(
    reply_id: UUID, 
    db: Session = Depends(get_db)
):
    return reply_service.delete_reply(reply_id=reply_id, db=db)