from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.schemas.user import UserCreate, UserResponse
from forum_system_api.services import user_service


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserResponse)
def register_user(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
) -> UserResponse:
    return user_service.create(user_data, db)
