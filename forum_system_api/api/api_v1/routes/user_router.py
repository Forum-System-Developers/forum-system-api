from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services import user_service
from forum_system_api.services.auth_service import get_current_user, require_admin_role
from forum_system_api.schemas.user import UserCreate, UserPermissionsResponse, UserResponse


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse)
def register_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
) -> UserResponse:
    return user_service.create(user_data, db)


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    return current_user


@router.get("/", response_model=list[UserResponse])
def get_all_users(
    admin: User = Depends(require_admin_role), 
    db: Session = Depends(get_db)
) -> list[UserResponse]:
    return user_service.get_all(db)


@router.get("/permissions/{category_id}", response_model=list[UserPermissionsResponse])
def view_privileged_users(
    category_id: UUID, 
    admin: User = Depends(require_admin_role), 
    db: Session = Depends(get_db)
) -> list[UserPermissionsResponse]:
    privileged_users = user_service.get_privileged_users(category_id=category_id, db=db)
    return [
        UserPermissionsResponse.create_response(user, permissions)
        for user, permissions in privileged_users.items()
    ]
