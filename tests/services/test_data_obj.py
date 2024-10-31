from tests.services import test_data_const as tc

USER_1 = {
    "id": tc.VALID_USER_ID,
    "username": tc.VALID_USERNAME,
    "password_hash": tc.VALID_PASSWORD_HASH,
    "email": tc.VALID_EMAIL,
    "first_name": tc.VALID_FIRST_NAME,
    "last_name": tc.VALID_LAST_NAME,
    "token_version": tc.VALID_TOKEN_VERSION,
    "created_at": tc.VALID_CREATED_AT,
}

USER_2 = {
    "id": tc.VALID_USER_ID_2,
    "username": tc.VALID_USERNAME_2,
    "password_hash": tc.VALID_PASSWORD_HASH_2,
    "email": tc.VALID_EMAIL_2,
    "first_name": tc.VALID_FIRST_NAME_2,
    "last_name": tc.VALID_LAST_NAME_2,
    "token_version": tc.VALID_TOKEN_VERSION_2,
    "created_at": tc.VALID_CREATED_AT_2,
}


VALID_TOPIC_1 = {
    "id": tc.VALID_TOPIC_ID_1,
    "title": tc.VALID_TOPIC_TITLE_1,
    "content": tc.VALID_TOPIC_CONTENT_1,
    "is_locked": tc.VALID_TOPIC_IS_LOCKED_1,
    "created_at": tc.VALID_TOPIC_CREATED_AT_1,
    "author_id": tc.VALID_AUTHOR_ID_1,
    "category_id": tc.VALID_TOPIC_CATEGORY_ID_1,
    "best_reply_id": tc.VALID_BEST_REPLY_ID_1,
}


VALID_TOPIC_2 = {
    "id": tc.VALID_TOPIC_ID_2,
    "title": tc.VALID_TOPIC_TITLE_2,
    "content": tc.VALID_TOPIC_CONTENT_2,
    "is_locked": tc.VALID_TOPIC_IS_LOCKED_2,
    "created_at": tc.VALID_TOPIC_CREATED_AT_2,
    "author_id": tc.VALID_AUTHOR_ID_2,
    "category_id": tc.VALID_TOPIC_CATEGORY_ID_2,
    "best_reply_id": tc.VALID_BEST_REPLY_ID_2,
}


VALID_CATEGORY_1 = {
    "id": tc.VALID_CATEGORY_ID_1,
    "name": tc.VALID_CATEGORY_NAME_1,
    "is_private": tc.VALID_CATEGORY_IS_PRIVATE_1,
    "is_locked": tc.VALID_CATEGORY_IS_LOCKED_1,
    "created_at": tc.VALID_CATEGORY_CREATED_AT_1,
}

VALID_CATEGORY_2 = {
    "id": tc.VALID_CATEGORY_ID_2,
    "name": tc.VALID_CATEGORY_NAME_2,
    "is_private": tc.VALID_CATEGORY_IS_PRIVATE_2,
    "is_locked": tc.VALID_CATEGORY_IS_LOCKED_2,
    "created_at": tc.VALID_CATEGORY_CREATED_AT_2,
}


VALID_TOPIC_FILTER_PARAMS = {
    "order": "asc",
    "order_by": "created_at",
    "limit": 20,
    "offset": 0,
}


VALID_REPLY = {
    "id": tc.VALID_REPLY_ID,
    "content": tc.VALID_REPLY_CONTENT,
    "author_id": tc.VALID_REPLY_AUTHOR_ID,
    "topic_id": tc.VALID_REPLY_TOPIC_ID,
    "created_at": tc.VALID_REPLY_CREATED_AT,
}


VALID_REPLY_REACTION_CREATE_TRUE = {"reaction": True}


VALID_REPLY_REACTION_CREATE_FALSE = {"reaction": True}

VALID_REPLY_REACTION_TRUE = {
    "user_id": tc.VALID_USER_ID,
    "reply_id": tc.VALID_REPLY_ID,
    "reaction": True,
    "created_at": tc.VALID_REPLY_CREATED_AT,
}


VALID_REPLY_CREATE = {
    "content": tc.VALID_REPLY_CONTENT,
}

VALID_TOPIC_CREATE = {
    "title": tc.VALID_TOPIC_TITLE_1,
    "content": tc.VALID_TOPIC_CONTENT_1,
}
