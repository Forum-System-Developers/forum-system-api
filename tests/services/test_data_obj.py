from tests.services import test_data_const as tc

USER_1 = {
    "id": tc.VALID_USER_ID,
    "username": tc.VALID_USERNAME,
    "password_hash": tc.VALID_PASSWORD_HASH,
    "email": tc.VALID_EMAIL,
    "first_name": tc.VALID_FIRST_NAME,
    "last_name": tc.VALID_LAST_NAME,
    "token_version": tc.VALID_TOKEN_VERSION,
    "created_at": tc.VALID_CREATED_AT
}

USER_2 = {
    "id": tc.VALID_USER_ID_2,
    "username": tc.VALID_USERNAME_2,
    "password_hash": tc.VALID_PASSWORD_HASH_2,
    "email": tc.VALID_EMAIL_2,
    "first_name": tc.VALID_FIRST_NAME_2,
    "last_name": tc.VALID_LAST_NAME_2,
    "token_version": tc.VALID_TOKEN_VERSION_2,
    "created_at": tc.VALID_CREATED_AT_2
}


VALID_TOPIC_1 = {
    "id": tc.VALID_TOPIC_ID,
    "title": tc.VALID_TOPIC_TITLE,
    "is_locked": tc.VALID_TOPIC_IS_LOCKED,
    "created_at": tc.VALID_TOPIC_CREATED_AT,
    "author_id": tc.VALID_AUTHOR_ID,
    "category_id": tc.VALID_CATEGORY_ID,
    "best_reply_id": tc.VALID_BEST_REPLY_ID,
}
