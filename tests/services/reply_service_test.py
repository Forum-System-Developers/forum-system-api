import unittest
from unittest.mock import ANY, MagicMock, Mock, patch

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.category import Category
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.reply import ReplyCreate, ReplyUpdate
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

        with patch('forum_system_api.services.reply_service.category_permission', return_value=True):
            reply = reply_service.get_by_id(self.user, self.reply.id, self.db)

            self.assertEqual(reply, self.reply)

            self.db.query.assert_called_once_with(Reply)


    def test_getById_noReply_returns404(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None

        with patch('forum_system_api.services.reply_service.category_permission', return_value=True):
            with self.assertRaises(HTTPException) as context:
                reply_service.get_by_id(self.user, self.reply.id, self.db)

                self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(context.exception.detail, "Reply not found")
                self.db.query.assert_called_once_with(Reply)



    def test_getById_invalidCategoryPermission_raises403(self):
        with patch(
            "forum_system_api.services.reply_service.category_permission"
        ) as category_permission_mock:
            category_permission_mock.side_effect = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot fetch reply",
            )
            with self.assertRaises(HTTPException) as context:
                reply_service.get_by_id(self.user, self.reply.id, self.db)

            self.assertEqual(
                context.exception.status_code, status.HTTP_403_FORBIDDEN
            )
            self.assertEqual(context.exception.detail, "Cannot fetch reply")            




    def test_createReply_invalidReplyAccess_raises403(self):
        reply_create = ReplyCreate(content=tc.VALID_REPLY_CONTENT)

        with patch(
            "forum_system_api.services.reply_service._validate_reply_access"
        ) as valdate_reply_mock:
            valdate_reply_mock.side_effect = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot reply to this post",
            )
            with self.assertRaises(HTTPException) as context:
                reply_service.create(self.topic.id, reply_create, self.user, self.db)

            self.assertEqual(
                context.exception.status_code, status.HTTP_403_FORBIDDEN
            )
            self.assertEqual(context.exception.detail, 'Cannot reply to this post')
            
            
    def test_createReply_invalidCategoryPermission_raises403(self):
        reply_create = ReplyCreate(content=tc.VALID_REPLY_CONTENT)

        with patch(
            "forum_system_api.services.reply_service.category_permission"
        ) as category_permission_mock:
            category_permission_mock.side_effect = HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot reply to this post",
            )
            with self.assertRaises(HTTPException) as context:
                reply_service.create(self.topic.id, reply_create, self.user, self.db)

            self.assertEqual(
                context.exception.status_code, status.HTTP_403_FORBIDDEN
            )
            self.assertEqual(context.exception.detail, 'Cannot reply to this post')


    def test_update_updatesReply_content_authorIsUser(self):
        reply_update = ReplyUpdate(content=tc.VALID_REPLY_CONTENT_2)

        self.reply.author_id = self.user.id
        
        with patch('forum_system_api.services.reply_service.get_by_id', return_value=self.reply):
            updated_reply = reply_service.update(self.user, self.reply.id, reply_update, self.db)
            
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(self.reply)
            self.assertEqual(updated_reply.content, self.reply.content)
            
            

    def test_update_authorIsNotUser_raises403(self):
        reply_update = ReplyUpdate(content=tc.VALID_REPLY_CONTENT_2)

        self.reply.author_id = tc.VALID_USER_ID_2
        
        with patch('forum_system_api.services.reply_service.get_by_id', return_value=self.reply):
            
            with self.assertRaises(HTTPException) as context:
                reply_service.update(self.user, self.reply.id, reply_update, self.db)
                
                self.assertEqual(
                context.exception.status_code, status.HTTP_403_FORBIDDEN
            )
                self.assertEqual(context.exception.detail, 'Cannot reply to this post')