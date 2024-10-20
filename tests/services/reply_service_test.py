import unittest
from unittest.mock import ANY, MagicMock, Mock, patch

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.category import Category
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.user_category_permission import (
    UserCategoryPermission,
)
from forum_system_api.schemas.reply import ReplyCreate
from forum_system_api.services import reply_service
from forum_system_api.services.user_service import is_admin
from tests.services import test_data_const as tc
from tests.services import test_data_obj as tobj
from tests.services.utils import assert_filter_called_with


class ReplyServiceShould(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(**tobj.USER_1)
        self.reply = Reply(**tobj.VALID_REPLY)
        self.topic = Topic(**tobj.VALID_TOPIC_1)
        self.category = Category(**tobj.VALID_CATEGORY_1)

    def test_getById_returnsReply(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.reply

        topic = reply_service.get_by_id(self.reply.id, self.user, self.db)

        self.assertEqual(topic, self.reply)

        self.db.query.assert_called_once_with(Topic)

    def test_getById_noReply_returns404(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None

        with self.assertRaises(HTTPException) as context:
            reply_service.get_by_id(self.reply.id, self.db)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Reply not found")

        self.db.query.assert_called_once_with(Reply)

    def test_createReply_createsReply_validUserAccess(self):
        reply_create = ReplyCreate(content=tc.VALID_REPLY_CONTENT)

        with (
            patch(
                "forum_system_api.services.reply_service._validate_reply_access",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.reply_service.category_permission",
                return_value=True,
            ),
        ):
            new_reply = reply_service.create(
                self.topic.id, reply_create, self.user, self.db
            )

            self.db.add.assert_called_once_with(new_reply)
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(new_reply)
            self.assertEqual(new_reply.topic_id, self.topic.id)
            self.assertEqual(new_reply.author_id, self.user.id)
            self.assertEqual(new_reply.content, tc.VALID_REPLY_CONTENT)

    def test_createReply_invalidReplyAccess_raises401(self):
        reply_create = ReplyCreate(content=tc.VALID_REPLY_CONTENT)

        with patch(
            "forum_system_api.services.reply_service._validate_reply_access"
        ) as valdate_reply_mock:
            valdate_reply_mock.side_effect = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot reply to this post",
            )
            with self.assertRaises(HTTPException) as context:
                reply_service.create(self.topic.id, reply_create, self.user, self.db)

            self.assertEqual(
                context.exception.status_code, status.HTTP_401_UNAUTHORIZED
            )
            self.assertEqual(context.exception.detail, str(context.exception.detail))

    def test_createReply_invalidCategoryPermission_raises401(self):
        reply_create = ReplyCreate(content=tc.VALID_REPLY_CONTENT)

        with patch(
            "forum_system_api.services.reply_service.category_permission"
        ) as catwgory_permission_mock:
            catwgory_permission_mock.side_effect = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Cannot reply to this post",
            )
            with self.assertRaises(HTTPException) as context:
                reply_service.create(self.topic.id, reply_create, self.user, self.db)

            self.assertEqual(
                context.exception.status_code, status.HTTP_401_UNAUTHORIZED
            )
            self.assertEqual(context.exception.detail, str(context.exception.detail))
