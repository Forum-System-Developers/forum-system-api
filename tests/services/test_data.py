from uuid import uuid4
from datetime import datetime, timezone


VALID_USER_ID = uuid4()
VALID_USERNAME = "testuser"
VALID_PASSWORD = "password"
VALID_PASSWORD_HASH = "hashed_password"
VALID_EMAIL = "test_user@test.com"
VALID_FIRST_NAME = "Test"
VALID_LAST_NAME = "User"
VALID_TOKEN_VERSION = uuid4()
VALID_CREATED_AT = datetime.now(timezone.utc)

USER_1 = {
    "id": VALID_USER_ID,
    "username": VALID_USERNAME,
    "password_hash": VALID_PASSWORD_HASH,
    "email": VALID_EMAIL,
    "first_name": VALID_FIRST_NAME,
    "last_name": VALID_LAST_NAME,
    "token_version": VALID_TOKEN_VERSION,
    "created_at": VALID_CREATED_AT
}

VALID_USER_ID_2 = uuid4()
VALID_USERNAME_2 = "testuser2"
VALID_PASSWORD_HASH_2 = "hashed_password2"
VALID_EMAIL_2 = "test_user@test.com"
VALID_FIRST_NAME_2 = "Test"
VALID_LAST_NAME_2 = "User"
VALID_TOKEN_VERSION_2 = uuid4()
VALID_CREATED_AT_2 = datetime.now(timezone.utc)

USER_2 = {
    "id": VALID_USER_ID_2,
    "username": VALID_USERNAME_2,
    "password_hash": VALID_PASSWORD_HASH_2,
    "email": VALID_EMAIL_2,
    "first_name": VALID_FIRST_NAME_2,
    "last_name": VALID_LAST_NAME_2,
    "token_version": VALID_TOKEN_VERSION_2,
    "created_at": VALID_CREATED_AT_2
}
