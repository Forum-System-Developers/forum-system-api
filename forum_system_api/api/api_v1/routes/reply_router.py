from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.reply import (
    ReplyCreate,
    ReplyReactionCreate,
    ReplyResponse,
    ReplyUpdate,
)
from forum_system_api.services import reply_service
from forum_system_api.services.auth_service import get_current_user

reply_router = APIRouter(prefix="/replies", tags=["replies"])


@reply_router.get(
    "/{reply_id}",
    response_model=ReplyResponse,
    status_code=200,
    description="Get a reply by its ID",
)
def get_by_id(
    reply_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReplyResponse:
    reply = reply_service.get_by_id(user=user, reply_id=reply_id, db=db)
    votes = reply_service.get_votes(reply=reply)
    return ReplyResponse.create(reply=reply, votes=votes)


@reply_router.post(
    "/{topic_id}",
    response_model=ReplyResponse,
    status_code=201,
    description="Create a new reply for a topic",
)
def create(
    topic_id: UUID,
    reply: ReplyCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReplyResponse:
    reply = reply_service.create(topic_id=topic_id, reply=reply, user=user, db=db)
    votes = (0, 0)
    return ReplyResponse.create(reply=reply, votes=votes)


@reply_router.put(
    "/{reply_id}",
    response_model=ReplyResponse,
    status_code=201,
    description="Update the content of a reply",
)
def update(
    reply_id: UUID,
    updated_reply: ReplyUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReplyResponse:
    reply = reply_service.update(
        user=user, reply_id=reply_id, updated_reply=updated_reply, db=db
    )
    votes = reply_service.get_votes(reply=reply)
    return ReplyResponse.create(reply=reply, votes=votes)


@reply_router.patch(
    "/{reply_id}/vote",
    response_model=ReplyResponse,
    status_code=201,
    description="Upvote or Downvote a reply",
)
def create_reaction(
    reply_id: UUID,
    reaction: ReplyReactionCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReplyResponse:
    reply = reply_service.vote(reply_id=reply_id, reaction=reaction, user=user, db=db)
    votes = reply_service.get_votes(reply=reply)
    return ReplyResponse.create(reply=reply, votes=votes)
