from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from forum_system_api.services.auth_service import require_admin_role
from forum_system_api.services import category_service
from forum_system_api.services import topic_service
from forum_system_api.schemas.category import CreateCategory, CategoryResponse
from forum_system_api.schemas.topic import TopicResponse
from forum_system_api.schemas.common import FilterParams
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User


category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CreateCategory,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_role),
) -> CategoryResponse:
    return category_service.create_category(data, db)


@category_router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)) -> CategoryResponse:
    return category_service.get_all(db)


@category_router.get("/{category_id}/topics")
def view_category(
    category_id: UUID,
    filter_params: FilterParams = Depends(),
    db: Session = Depends(get_db),
) -> list[TopicResponse]:
    topics = topic_service.get_all(filter_params=filter_params, db=db)

    return [
        TopicResponse.create(
            topic=topic,
            replies=topic_service.get_replies(topic_id=topic.id, db=db),
        )
        for topic in topics
        if topic.category_id == category_id
    ]


@category_router.put("/{category_id}/private")
def make_category_private_or_public(
    category_id: UUID,
    is_private: bool,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_role),
) -> CategoryResponse:
    return category_service.make_private_or_public(category_id, is_private, db)


@category_router.put("/{category_id}/lock")
def lock_or_unlock_category(
    category_id: UUID,
    is_locked: bool,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_role),
) -> CategoryResponse:
    return category_service.lock_or_unlock(category_id, is_locked, db)
