from uuid import UUID

from fastapi import APIRouter, Depends, Path, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.token import Token
from forum_system_api.services import auth_service
from forum_system_api.services.auth_service import (
    get_current_user,
    oauth2_scheme,
    require_admin_role,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post(
    "/login",
    response_model=Token,
    description="Authenticate a user and generate access and refresh tokens.",
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> Token:
    user = auth_service.authenticate_user(
        username=form_data.username, password=form_data.password, db=db
    )
    return auth_service.create_access_and_refresh_tokens(user=user, db=db)


@auth_router.post(
    "/logout",
    description="Logs out the current user by invalidating their existing tokens.",
)
def logout_user(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    auth_service.update_token_version(user_id=current_user.id, db=db)
    return {"msg": "Successfully logged out"}


@auth_router.post(
    "/refresh",
    response_model=Token,
    description="Generates a new access token using the provided refresh token.",
)
def refresh_token(
    refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> Token:
    access_token = auth_service.refresh_access_token(refresh_token=refresh_token, db=db)

    return Token(
        access_token=access_token, refresh_token=refresh_token, token_type="bearer"
    )


@auth_router.put(
    "/revoke/{user_id}",
    description="This endpoint requires admin privileges and will invalidate \
                the tokens associated with the specified user.",
    dependencies=[Depends(require_admin_role)],
)
def revoke_token(
    user_id: UUID = Path(..., description="The unique identifier of the user"),
    db: Session = Depends(get_db),
) -> dict:
    auth_service.update_token_version(user_id=user_id, db=db)
    return {"msg": "Token revoked"}
