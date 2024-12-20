import logging
from datetime import datetime, timedelta
from typing import cast
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from forum_system_api.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    REFRESH_TOKEN_EXPIRE_DAYS,
    SECRET_KEY,
)
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.token import Token
from forum_system_api.services import user_service
from forum_system_api.services.user_service import is_admin
from forum_system_api.services.utils.password_utils import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
logger = logging.getLogger(__name__)


def create_access_token(data: dict) -> str:
    """
    Generates an access token with the given data and an expiration time.

    Args:
        data (dict): The data to be included in the token payload.

    Returns:
        str: The generated access token as a string.
    """
    access_token = create_token(
        data=data, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    logger.info(f"Generated access token for user {data.get('sub')}")

    return access_token


def create_refresh_token(data: dict) -> str:
    """
    Generates a refresh token with the provided data and a predefined expiration time.

    Args:
        data (dict): The data to be included in the refresh token.

    Returns:
        str: The generated refresh token as a string.
    """
    refresh_token = create_token(
        data=data, expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )
    logger.info(f"Generated refresh token for user {data.get('sub')}")

    return refresh_token


def create_token(data: dict, expires_delta: timedelta) -> str:
    """
    Creates a JSON Web Token (JWT) with the given data and expiration delta.

    Args:
        data (dict): The payload data to include in the token.
        expires_delta (timedelta): The time duration after which the token will expire.

    Returns:
        str: The encoded JWT as a string.

    Raises:
        HTTPException: If there is an error in creating the token.
    """
    payload = data.copy()
    expire = datetime.now() + expires_delta
    payload.update({"exp": expire})
    try:
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        logger.info(f"Creating token with payload: {payload}")
        return token
    except JWTError:
        logger.error(f"Could not create token with payload: {payload}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create token",
        )


def create_access_and_refresh_tokens(user: User, db: Session) -> Token:
    """
    Generates access and refresh tokens for a given user.

    Args:
        user (User): The user object for whom the tokens are being created.
        db (Session): The database session used to update the token version.

    Returns:
        Token: An object containing the access and refresh tokens and their type.
    """
    token_data = create_token_data(user=user, db=db)
    logger.info(f"Created token data for user {user.id}")
    access_token = create_access_token(token_data)
    logger.info(f"Created access token for user {user.id}")
    refresh_token = create_refresh_token(token_data)
    logger.info(f"Created refresh token for user {user.id}")

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


def refresh_access_token(refresh_token: str, db: Session) -> str:
    """
    Refreshes the access token using the provided refresh token.

    Args:
        refresh_token (str): The refresh token used to generate a new access token.
        db (Session): The database session used for token verification.

    Returns:
        str: A new access token.
    """
    payload = verify_token(token=refresh_token, db=db)
    user_id = payload.get("sub")
    token_version = payload.get("token_version")
    is_admin = payload.get("is_admin")
    logger.info(f"Verified refresh token for user {user_id}")

    access_token = create_access_token(
        {"sub": user_id, "token_version": token_version, "is_admin": is_admin}
    )
    logger.info(f"Created new access token for user {user_id}")

    return access_token


def verify_token(token: str, db: Session) -> dict:
    """
    Verifies the provided JWT token and returns the payload if valid.

    Args:
        token (str): The JWT token to be verified.
        db (Session): The database session to use for querying user information.

    Returns:
        dict: The decoded payload from the JWT token if verification is successful.

    Raises:
        HTTPException: If the token cannot be verified or if the user associated with the token cannot be found or has an invalid token version.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded token payload: {payload}")
    except JWTError:
        logger.error("Could not verify token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify token"
        )

    user_id = UUID(payload.get("sub"))
    token_version = UUID(payload.get("token_version"))
    user = user_service.get_by_id(user_id=user_id, db=db)

    if user is None:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify token"
        )
    logger.info(f"Retrieved user {user_id}")

    if user.token_version != token_version:
        logger.error(f"Invalid token version for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not verify token"
        )

    return payload


def update_token_version(user_id: UUID, db: Session) -> UUID:
    """
    Updates the token version for a given user.

    Args:
        user_id (UUID): The unique identifier of the user.
        db (Session): The database session to use for committing the changes.

    Returns:
        UUID: The new token version of the user.

    Raises:
        HTTPException: If the user is not found.
    """
    user = user_service.get_by_id(user_id=user_id, db=db)
    if user is None:
        logger.error("User not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    user.token_version = uuid4()
    db.commit()
    db.refresh(user)
    logger.info(f"Updated token version for user {user.id}")

    return user.token_version


def authenticate_user(username: str, password: str, db: Session) -> User:
    """
    Authenticate a user by their username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.
        db (Session): The database session.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the user cannot be authenticated due to incorrect username or password.
    """
    user = user_service.get_by_username(username=username, db=db)

    if user is None:
        logger.error(f"User with username {username} not found")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not authenticate user",
        )
    logger.info(f"Retrieved user {user.id} with username {username}")

    verified_password = verify_password(password, user.password_hash)

    if not verified_password:
        logger.error(f"Invalid password for user {user.id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not authenticate user",
        )
    logger.info(f"Password verified for user {user.id}")

    return user


def authenticate_websocket_user(data: dict, db: Session) -> UUID | None:
    """
    Authenticate a user by their WebSocket connection data.

    Args:
        data (dict): The WebSocket connection data.
        db (Session): The database session.

    Returns:
        UUID: The unique identifier of the authenticated user.
    """
    if data.get("type") != "auth" or data.get("token") is None:
        logger.error(f"Invalid WebSocket authentication data {data}")
        return None

    token = data["token"]
    try:
        payload = verify_token(token=token, db=db)
    except HTTPException:
        logger.error(f"Could not verify WebSocket token {token}")
        return None

    logger.info(f"Authenticated WebSocket user {payload.get('sub')}")
    return UUID(payload.get("sub"))


def create_token_data(user: User, db: Session) -> dict:
    """
    Generates token data for a given user.

    Args:
        user (User): The user object for whom the token data is being created.
        db (Session): The database session used for querying and updating the database.

    Returns:
        dict: A dictionary containing the token data with the following keys:
            - "sub": The user ID as a string.
            - "token_version": The token version as a string.
            - "is_admin": A boolean indicating whether the user has admin privileges.
    """
    token_version = update_token_version(user_id=user.id, db=db)
    token_data = {
        "sub": str(user.id),
        "token_version": str(token_version),
        "is_admin": is_admin(user_id=user.id, db=db),
    }
    logger.info(f"Created token data for user {user.id}")

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    Retrieve the current user based on the provided token.

    Args:
        token (str): The authentication token provided by the user.
        db (Session): The database session dependency.

    Returns:
        User: The user object corresponding to the token.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    token_data = verify_token(token=token, db=db)
    user_id = cast(UUID, UUID(token_data.get("sub")))

    user = user_service.get_by_id(user_id=user_id, db=db)
    if user is None:
        logger.error(f"User with ID {user_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    logger.info(f"Retrieved current user {user_id}")

    return user


def require_admin_role(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> User:
    """
    Dependency that ensures the current user has an admin role.

    Args:
        user (User): The current user, obtained from the `get_current_user` dependency.
        db (Session): The database session, obtained from the `get_db` dependency.

    Returns:
        User: The current user if they have an admin role.

    Raises:
        HTTPException: If the current user does not have an admin role, with a 403 Forbidden status code.
    """
    is_admin = user_service.is_admin(user_id=user.id, db=db)

    if not is_admin:
        logger.error(f"User {user.id} does not have admin privileges")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    logger.info(f"User {user.id} has admin privileges")

    return user
