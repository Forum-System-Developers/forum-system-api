from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services import auth_service, user_service
from forum_system_api.services.auth_service import get_current_user, oauth2_scheme
from forum_system_api.schemas.token import Token

 
auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
) -> Token:
    user = auth_service.authenticate_user(form_data.username, form_data.password, db=db)
    token_version = user_service.update_token_version(user=user, db=db)
    token_data = {"sub": str(user.id), "token_version": str(token_version)}
    access_token = auth_service.create_access_token(token_data)
    refresh_token = auth_service.create_refresh_token(token_data)

    return Token(
        access_token=access_token, 
        refresh_token=refresh_token, 
        token_type="bearer"
    )


@auth_router.post("/logout")
def logout_user(
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
) -> Response:
    user_service.update_token_version(user=current_user, db=db)
    return {"msg": "Successfully logged out"}


@auth_router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> Token:
    access_token = auth_service.refresh_access_token(refresh_token=refresh_token, db=db)

    return Token(
        access_token=access_token, 
        refresh_token=refresh_token, 
        token_type="bearer"
    )
