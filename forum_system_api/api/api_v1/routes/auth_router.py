from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from forum_system_api.schemas.common import FilterParams
from forum_system_api.schemas.token import Token
from forum_system_api.schemas.topic import TopicResponse, TopicCreate, TopicUpdate
from forum_system_api.persistence.database import get_db
from forum_system_api.services.auth_service import oauth2_scheme
from forum_system_api.services.auth_service import create_access_token, create_refresh_token, authenticate_user


auth_router = APIRouter(prefix='/', tags=["login"])

@auth_router.post('/login', status_code=200)
def login(
    username: str,
    password: str,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Token:
    user = authenticate_user(username=username, password=password, db=db)
    access_token = create_access_token(user=user)