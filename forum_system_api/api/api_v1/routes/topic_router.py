from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from forum_system_api.schemas.common import FilterParams
from forum_system_api.schemas.topic import TopicResponse, TopicCreate, TopicUpdate, TopicLock
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services import topic_service
from forum_system_api.services.auth_service import get_current_user, require_admin_role


topic_router = APIRouter(prefix='/topics', tags=["topics"])


@topic_router.get('/all', response_model=list[TopicResponse], status_code=200)
def get_all(
    filter_query: FilterParams = Depends(),
    db: Session = Depends(get_db)
) -> list[TopicResponse]:
    topics = topic_service.get_all(filter_params=filter_query, db=db)
    return [
        TopicResponse.create(
            topic=topic,
            replies=topic_service.get_replies(topic_id=topic.id, db=db),
        ) for topic in topics]
    

@topic_router.get('/{topic_id}', response_model=TopicResponse, status_code=200)
def get_by_id(
    topic_id: UUID,
    db: Session = Depends(get_db)
) -> TopicResponse:
    topic = topic_service.get_by_id(topic_id=topic_id, db=db)
    return TopicResponse.create(
        topic=topic,
        replies=topic_service.get_replies(topic_id=topic.id, db=db),
    )
    

@topic_router.post('/create', response_model=TopicResponse, status_code=201)
def create(
    topic: TopicCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TopicResponse:
    topic = topic_service.create(topic=topic, user_id=user.id, db=db)
    return TopicResponse.create(
        topic=topic,
        replies=[]
    )


@topic_router.put('/{topic_id}/edit', response_model=TopicResponse, status_code=201)
def update(
    topic_id: UUID, 
    updated_topic: TopicUpdate, 
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TopicResponse:
    topic = topic_service.update(user=user, topic_id=topic_id, updated_topic=updated_topic, db=db)
    return TopicResponse.create(
        topic=topic,
        replies=topic_service.get_replies(topic_id=topic.id, db=db),
    )


@topic_router.put('/{topic_id}/lock', status_code=201)
def lock(
    topic_id: UUID, 
    lock_topic: TopicLock,
    admin: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
) -> dict:
    topic = topic_service.lock(topic_id=topic_id, lock_topic=lock_topic, db=db)
    return {"msg": "Topic locked"} if topic.is_locked else {"msg": "Unlocked"}


@topic_router.put('/{topic_id}/select_best', response_model=TopicResponse, status_code=201)
def best_reply(
    topic_id: UUID,
    reply_id: UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TopicResponse:
    topic = topic_service.select_best_reply(user=user, topic_id=topic_id, reply_id=reply_id, db=db)
    return TopicResponse.create(
        topic=topic,
        replies=topic_service.get_replies(topic_id=topic.id, db=db)
    )
