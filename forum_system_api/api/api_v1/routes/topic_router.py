from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from forum_system_api.schemas.common import FilterParams
from forum_system_api.schemas.topic import TopicResponse, TopicCreate, TopicUpdate
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services.auth_service import oauth2_scheme, get_current_user
from forum_system_api.services import topic_service


topic_router = APIRouter(prefix='/topics', tags=["topics"])


@topic_router.get('/', response_model=list[TopicResponse], status_code=200)
def get_all(
    filter_query: FilterParams = Depends(),
    db: Session = Depends(get_db)
) -> list[TopicResponse]:
    return topic_service.get_all(filter_params=filter_query, db=db)


@topic_router.get('/{topic_id}', response_model=TopicResponse, status_code=200)
def get_by_id(
    topic_id: UUID,
    db: Session = Depends(get_db)
) -> TopicResponse:
    return topic_service.get_by_id(topic_id=topic_id, db=db)
    

@topic_router.post('/', response_model=TopicResponse, status_code=201)
def create(
    topic: TopicCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TopicResponse:
    return topic_service.create(topic=topic, user_id=user.id, db=db)


@topic_router.put('/', response_model=TopicResponse, status_code=201)
def update(
    topic_id: UUID, 
    updated_topic: TopicUpdate, 
    db: Session = Depends(get_db)
) -> TopicResponse:
    return topic_service.update(topic_id=topic_id, updated_topic=updated_topic, db=db)
