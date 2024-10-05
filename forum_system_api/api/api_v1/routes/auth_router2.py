from uuid import UUID

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from sqlalchemy.orm import Session

from forum_system_api.schemas.common import FilterParams
from forum_system_api.schemas.token import Token
from forum_system_api.schemas.topic import TopicResponse, TopicCreate, TopicUpdate
from forum_system_api.persistence.database import get_db
from forum_system_api.services.auth_service2 import oauth2_scheme
from forum_system_api.services.auth_service2 import create_access_token, create_refresh_token, authenticate_user


auth_router = APIRouter(prefix='/auth', tags=["authentication"])


@auth_router.post('/login', status_code=200, response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)
    access_token = create_access_token(user=user)
    refresh_token = create_refresh_token(user=user)
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )