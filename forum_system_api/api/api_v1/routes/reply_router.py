from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from forum_system_api.schemas.common import FilterParams
from forum_system_api.schemas.reply import ReplyResponse, ReplyCreate, ReplyUpdate, ReplyReactionCreate
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services import reply_service
from forum_system_api.services.auth_service import get_current_user


reply_router = APIRouter(prefix='/replies', tags=["replies"])


@reply_router.get('/{topic_id}', response_model=list[ReplyResponse], status_code=200)
def get_all_for_topic(
    topic_id: UUID,
    filter_query: FilterParams = Depends(),
    db: Session = Depends(get_db)
) -> list[ReplyResponse]:
    return reply_service.get_all(filter_params=filter_query, topic_id=topic_id, db=db)


@reply_router.get('/{reply_id}', response_model=ReplyResponse, status_code=200)
def get_by_id(
    reply_id: UUID,
    db: Session = Depends(get_db)
) -> ReplyResponse:
    reply = reply_service.get_by_id(reply_id=reply_id, db=db)
    votes = reply_service.get_votes(reply=reply, db=db)
    return ReplyResponse(
        upvotes = votes[0],
        downvotes = votes[1],
        **reply.__dict__
    )


@reply_router.post('/', response_model=ReplyResponse, status_code=201)
def create(
    topic_id: UUID,
    reply: ReplyCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> ReplyResponse:
    reply = reply_service.create(topic_id=topic_id, reply=reply, user_id=user.id, db=db)
    return ReplyResponse(
        **reply.__dict__,
        upvotes=0,
        downvotes=0
    )


@reply_router.put('/', response_model=ReplyResponse, status_code=201)
def update(
    reply_id: UUID, 
    updated_reply: ReplyUpdate, 
    db: Session = Depends(get_db)
) -> ReplyResponse:
    reply = reply_service.update(reply_id=reply_id, updated_reply=updated_reply, db=db)
    votes = reply_service.get_votes(reply=reply, db=db)
    return ReplyResponse(
        upvotes=votes[0],
        downvotes=votes[1],
        **reply.model_dump()
    )


@reply_router.post('/{reply_id}/vote', response_model=ReplyResponse, status_code=201)
def create_reaction(
    reply_id: UUID,
    reaction: ReplyReactionCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)    
) -> ReplyResponse:
    reply = reply_service.vote(
        reply_id=reply_id,
        reaction=reaction,
        user=user,
        db=db
    )
    votes = reply_service.get_votes(reply=reply, db=db)
    return ReplyResponse(
        upvotes = votes[0],
        downvotes = votes[1],
        **reply.__dict__
    )

