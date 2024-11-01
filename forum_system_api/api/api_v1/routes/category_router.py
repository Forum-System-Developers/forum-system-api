from uuid import UUID

from fastapi import APIRouter, Path, Query
from fastapi import Depends
from sqlalchemy.orm import Session

from forum_system_api.services.auth_service import require_admin_role, get_current_user
from forum_system_api.services import category_service
from forum_system_api.services import topic_service
from forum_system_api.schemas.category import CreateCategory, CategoryResponse
from forum_system_api.schemas.topic import TopicResponse
from forum_system_api.schemas.common import FilterParams
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User


category_router = APIRouter(prefix="/categories", tags=["categories"])


@category_router.post(
        "/", 
        response_model=CategoryResponse, 
        status_code=201, 
        description="Create a new category"
)
def create_category(
    data: CreateCategory,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_role),
) -> CategoryResponse:
    return category_service.create_category(data, db)


@category_router.get(
        "/", 
        response_model=list[CategoryResponse], 
        description="Get all categories"
)
def get_categories(db: Session = Depends(get_db)) -> CategoryResponse:
    return category_service.get_all(db)


@category_router.get(
        "/{category_id}/topics", 
        response_model=list[TopicResponse], 
        description="Get all topics for a category"
)
def view_category(
    category_id: UUID = Path(..., description="The unique identifier of the category"),
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> list[TopicResponse]:
    topics = topic_service.get_topics_for_category(category_id, user, db)
    return [
        TopicResponse.create(
            topic=topic,
            replies=topic_service.get_replies(topic_id=topic.id, db=db),
        )
        for topic in topics
    ]


@category_router.put(
        "/{category_id}/private", 
        response_model=CategoryResponse, 
        description="Make a category private or public"
)
def make_category_private_or_public(
    category_id: UUID = Path(..., description="The unique identifier of the category"),
    is_private: bool = Query(..., description="True if the category should be private, False if it should be public"),
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_role),
) -> CategoryResponse:
    return category_service.make_private_or_public(category_id, is_private, db)


@category_router.put(
        "/{category_id}/lock", 
        response_model=CategoryResponse, 
        description="Lock or unlock a category"
)
def lock_or_unlock_category(
    category_id: UUID = Path(..., description="The unique identifier of the category"),
    is_locked: bool = Query(..., description="True if the category should be locked, False if it should be unlocked"),
    db: Session = Depends(get_db),
    user: User = Depends(require_admin_role),
) -> CategoryResponse:
    return category_service.lock_or_unlock(category_id, is_locked, db)
