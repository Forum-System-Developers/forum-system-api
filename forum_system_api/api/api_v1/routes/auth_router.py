from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services import auth_service
from forum_system_api.schemas.token import Token


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
) -> Token:
    user = auth_service.authenticate_user(form_data.username, form_data.password, db=db)
    access_token = auth_service.create_access_token(user=user, db=db)
    refresh_token = auth_service.create_refresh_token(user)

    return Token(
        access_token=access_token, 
        refresh_token=refresh_token, 
        token_type="bearer"
    )
