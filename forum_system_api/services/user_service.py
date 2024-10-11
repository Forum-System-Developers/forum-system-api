from uuid import UUID
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.access_level import AccessLevel
from forum_system_api.persistence.models.admin import Admin
from forum_system_api.services import category_service
from forum_system_api.persistence.models.user_category_permission import UserCategoryPermission
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


def is_admin(user_id: UUID, db: Session) -> bool:
    return (db.query(Admin)
            .filter(Admin.user_id == user_id)
            .first()) is not None


def get_privileged_users(category_id: UUID, db: Session) -> dict[User, UserCategoryPermission]:
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

    return {permission.user: permission for permission in category.permissions}

def get_user_permissions(user_id: UUID, db: Session) -> list[UserCategoryPermission]:
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
    
    permission = next((p for p in category.permissions if p.user_id == user_id), None)
    
    if permission is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Permission not found"
        )
    
    db.delete(permission)
    db.commit()

    return True


def update_access_level(
        user_id: UUID, 
        category_id: UUID, 
        access_level: AccessLevel, 
        db: Session
) -> UserCategoryPermission:
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
    
    permission = next((p for p in category.permissions if p.user_id == user_id), None)
    
    if permission is None:
        permission = UserCategoryPermission(
            user_id=user_id,
            category_id=category_id, 
            access_level=access_level
        )
        category.permissions.append(permission)
    else:
        permission.access_level = access_level

    db.commit()
    db.refresh(permission)

    return permission
