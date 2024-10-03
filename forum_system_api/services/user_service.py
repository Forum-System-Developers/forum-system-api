from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import UUID

from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.user import UserCreate
from forum_system_api.services.utils.password_utils import hash_password


def get_by_id(user_id: UUID, db: Session) -> Optional[User]:
    return (db.query(User)
            .filter(User.id == user_id)
            .first())

def get_by_username(username: str, db: Session) -> Optional[User]:
    return (db.query(User)
            .filter(User.username == username)
            .first())


def get_by_email(email: str, db: Session) -> Optional[User]:
    return (db.query(User)
            .filter(User.email == email)
            .first())

def create(user_data: UserCreate, db: Session) -> User:    
    if get_by_username(user_data.username, db) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username already exists"
        )
    
    if get_by_email(user_data.email, db) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Email already exists"
        )
    
    hashed_password = hash_password(user_data.password)
    
    user = User(
        password_hash=hashed_password,
        **user_data.model_dump(exclude={"password"})
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user
