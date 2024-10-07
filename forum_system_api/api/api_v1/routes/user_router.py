from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.user import UserCreate, UserResponse
from forum_system_api.services import user_service
from forum_system_api.services.auth_service import require_admin_role


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse)
def register_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
) -> UserResponse:
    return user_service.create(user_data, db)

@router.get("/", response_model=list[UserResponse])
def get_all_users(
    admin: User = Depends(require_admin_role),
    db: Session = Depends(get_db)
) -> list[UserResponse]:
    return user_service.get_all(db)
