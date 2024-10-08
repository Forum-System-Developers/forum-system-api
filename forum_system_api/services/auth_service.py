from uuid import UUID
from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from forum_system_api.services import user_service
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services.utils.password_utils import verify_password
from forum_system_api.config import (
    SECRET_KEY, 
    ALGORITHM, 
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    REFRESH_TOKEN_EXPIRE_DAYS
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(data: dict) -> str:
    try:
        payload = data.copy()
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({'exp': expire})
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=500, detail='Could not create token')
    

def create_refresh_token(data: dict) -> str:
    try:
        payload = data.copy()
        expire = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
        payload.update({'exp': expire})
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=500, detail='Could not create token')


def refresh_access_token(refresh_token: str, db: Session) -> str:
    payload = verify_token(token=refresh_token, db=db)
    user_id = payload.get('sub')
    user = user_service.get_by_id(user_id=UUID(user_id), db=db)
    if user is None:
        raise HTTPException(status_code=401, detail='Could not verify token')
    access_token = create_access_token({
        'sub': user_id, 
        'token_version': str(user.token_version)
    })

    return access_token

def verify_token(token: str, db: Session) ->  dict:
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = UUID(payload.get('sub'))
        token_version = UUID(payload.get('token_version'))
        user = user_service.get_by_id(user_id=user_id, db=db)
        if user is None:
            raise HTTPException(status_code=401, detail='Could not verify token')
        if user.token_version != token_version:
            raise HTTPException(status_code=401, detail='Could not verify token')
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not verify token')
    

def revoke_token(user_id: UUID, db: Session) -> None:
    user = user_service.get_by_id(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    user_service.update_token_version(user=user, db=db)


def authenticate_user(username: str, password: str, db: Session) -> User:
    user = user_service.get_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=401, detail='Could not authenticate user')
    
    verified_password = verify_password(password, user.password_hash)
    if not verified_password:
        raise HTTPException(status_code=401, detail='Could not authenticate user')
    
    return user


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    token_data = verify_token(token=token, db=db)
    user = user_service.get_by_id(token_data.get("sub"), db=db)

    if user is None:
        raise HTTPException(status_code=401, detail='Could not authenticate user')

    return user


def require_admin_role(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
    is_admin = user_service.is_admin(user.id, db)

    if not is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    return user
