from uuid import UUID, uuid4
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.admin import Admin
from forum_system_api.services import category_service
from forum_system_api.persistence.models.category_permission import CategoryPermission
from forum_system_api.persistence.models.user import User
from forum_system_api.services.utils.password_utils import hash_password
from forum_system_api.schemas.user import UserCreate


def get_all(db: Session) -> list[User]:
    return db.query(User).all()


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


def update_token_version(user: User, db: Session) -> UUID:
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    user.token_version = uuid4()
    db.commit()
    db.refresh(user)

    return user.token_version


def is_admin(user_id: UUID, db: Session) -> bool:
    return (db.query(Admin)
            .filter(Admin.user_id == user_id)
            .first()) is not None


def get_privileged_users(category_id: UUID, db: Session) -> dict[User, CategoryPermission]:
    category = category_service.get_by_id(category_id=category_id, db=db)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )
    if not category.is_private:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Category is not private"
        )
    
    privileged_users = {}
    for permission in category.permissions:
        privileged_users[permission.user] = permission

    return privileged_users

def get_user_permissions(user_id: UUID, db: Session) -> list[CategoryPermission]:
    user = get_by_id(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    return user.permissions


def revoke_access(user_id: UUID, category_id: UUID, db: Session) -> bool:
    user = get_by_id(user_id=user_id, db=db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    category = category_service.get_by_id(category_id=category_id, db=db)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Category not found"
        )
    
    permission = (category.permissions
                  .filter(CategoryPermission.user_id == user_id)
                  .first())
    
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Permission not found"
        )
    
    db.delete(permission)
    db.commit()

    return True
