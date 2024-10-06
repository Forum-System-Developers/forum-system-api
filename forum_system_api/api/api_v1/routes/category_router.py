from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from forum_system_api.schemas.common import FilterParams
from forum_system_api.schemas.category import CategoryResponse, CreateCategory
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services import category_service
from forum_system_api.services.auth_service import get_current_user


category_router = APIRouter(prefix='/categories', tags=["categories"])
 

@category_router.get('/{category_id}', response_model=CategoryResponse, status_code=200)
def get_by_id(
    category_id: UUID,
    db: Session = Depends(get_db)
) -> CategoryResponse:
    return category_service.get_by_id(category_id=category_id, db=db)


 
@category_router.get("/", response_model=list[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db)
) -> CategoryResponse:
    categories = category_service.get_all(db=db)
 
    if categories is None:
        raise HTTPException(status_code=404, detail="There are no categories yet")
 
    return categories
 


@category_router.post("/", response_model=CategoryResponse)
def create_category(
    data: CreateCategory,
    db: Session = Depends(get_db),
    # user: User = Depends(require_admin_role)
) -> CategoryResponse:
    return category_service.create_category(data, db)