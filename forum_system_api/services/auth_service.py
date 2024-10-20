from uuid import UUID, uuid4
from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


def create_access_token(data: dict) -> str:
    return create_token(
        data=data, 
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    

def create_refresh_token(data: dict) -> str:
    return create_token(
        data=data, 
        expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    

def create_token(data: dict, expires_delta: timedelta) -> str:
    try:
        payload = data.copy()
        expire = datetime.now() + expires_delta
        payload.update({'exp': expire})
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail='Could not create token'
        )


def refresh_access_token(refresh_token: str, db: Session) -> str:
    payload = verify_token(token=refresh_token, db=db)
    user_id = payload.get('sub')
    token_version = payload.get('token_version')
    
    return create_access_token({
        'sub': user_id, 
        'token_version': token_version
    })


def verify_token(token: str, db: Session) ->  dict:
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = UUID(payload.get('sub'))
        token_version = UUID(payload.get('token_version'))
        user = user_service.get_by_id(user_id=user_id, db=db)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Could not verify token'
            )
        if user.token_version != token_version:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Could not verify token'
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Could not verify token'
        )
    
    
def update_token_version(user: User, db: Session) -> UUID:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail='User not found'
        )
    
    user.token_version = uuid4()
    db.commit()
    db.refresh(user)

    return user.token_version


def authenticate_user(username: str, password: str, db: Session) -> User:
    user = user_service.get_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Could not authenticate user'
        )
    
    verified_password = verify_password(password, user.password_hash)
    if not verified_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Could not authenticate user'
        )
    
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    token_data = verify_token(token=token, db=db)
    user = user_service.get_by_id(user_id=token_data.get('sub'), db=db)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Could not authenticate user'
        )

    return user


def require_admin_role(
    user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
) -> User:
    is_admin = user_service.is_admin(user_id=user.id, db=db)

    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail='Access denied'
        )

    return user
