from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from forum_system_api.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from forum_system_api.persistence.models.user import User
from forum_system_api.services.utils.password_utils import verify_password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_access_token(data: dict) -> str:
    try:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except JWTError:
        raise HTTPException(status_code=500, detail='Could not create token')


def create_refresh_token(data: dict) -> str:
    try:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=500, detail='Could not create token')


def verify_token(token: str) ->  dict:
    try:        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail='Could not verify token')
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail='Could not verify token')
    
    
def authenticate_user(username: str, password: str, db: Session) -> User:
    from forum_system_api.services import user_service
    
    user = user_service.get_by_username(username=username, db=db)
    if user is None:
        raise HTTPException(status_code=401, detail='Could not authenticate user')
    
    verified_password = verify_password(password, user.password_hash)
    if not verified_password:
        raise HTTPException(status_code=401, detail='Could not authenticate user')
    
    return user
