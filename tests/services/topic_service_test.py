import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.category import Category
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.user_category_permission import (
    UserCategoryPermission,
)
from forum_system_api.schemas.common import TopicFilterParams
from forum_system_api.schemas.topic import TopicCreate, TopicUpdate
from forum_system_api.services import topic_service
from tests.services import test_data_const as td
from tests.services import test_data_obj as tobj
from tests.services.utils import assert_filter_called_with


class TopicServiceShould(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(**tobj.USER_1)
        self.topic = Topic(**tobj.VALID_TOPIC_1)
        self.topic2 = Topic(**tobj.VALID_TOPIC_2)
        self.reply = Reply(**tobj.VALID_REPLY)
        self.category = Category(**tobj.VALID_CATEGORY_1)
        self.category2 = Category(**tobj.VALID_CATEGORY_2)
        self.filter_params = TopicFilterParams(**tobj.VALID_TOPIC_FILTER_PARAMS)
        self.permission = UserCategoryPermission(
            user_id=self.user.id,
            category_id=self.category.id,
            access_level=td.VALID_ACCESS_LEVEL_1,
        )

    def test_get_all_returnsAllTopics_userIsAdmin(self):
        self.topic.category_id = self.category.id
        self.topic2.category_id = self.category2.id

        self.user.permissions = [self.permission]

        query_mock = self.db.query.return_value
        join_mock = query_mock.join.return_value
        filter_mock = join_mock.filter.return_value
        order_by_mock = filter_mock.order_by.return_value
        offset_mock = order_by_mock.offset.return_value
        limit_mock = offset_mock.limit.return_value
        limit_mock.all.return_value = [self.topic, self.topic2]

        expected = [self.topic, self.topic2]

        with (
            patch(
                "forum_system_api.services.topic_service.is_admin", return_value=True
            ),
            patch(
                "forum_system_api.services.topic_service.getattr",
                return_value=Topic.created_at,
            ),
        ):
            topics = topic_service.get_all(self.filter_params, self.user, self.db)

            self.assertEqual(topics, expected)
            self.db.query.assert_called_once_with(Topic)
            order_by_mock.offset.assert_called_once_with(self.filter_params.offset)
            offset_mock.limit.assert_called_once_with(self.filter_params.limit)

    def test_get_all_returnsTopics_permissions_userNotAdmin(self):
        self.topic.category_id = self.category.id
        self.topic2.category_id = self.category2.id

        self.user.permissions = [self.permission]

        query_mock = self.db.query.return_value
        join_mock = query_mock.join.return_value
        filter_mock = join_mock.filter.return_value
        order_by_mock = filter_mock.order_by.return_value
        offset_mock = order_by_mock.offset.return_value
        limit_mock = offset_mock.limit.return_value
        limit_mock.all.return_value = [self.topic]

        expected = [self.topic]

        with (
            patch(
                "forum_system_api.services.topic_service.is_admin", return_value=False
            ),
            patch(
                "forum_system_api.services.topic_service.getattr",
                return_value=Topic.created_at,
            ),
        ):
            topics = topic_service.get_all(self.filter_params, self.user, self.db)

            self.assertEqual(topics, expected)
            self.db.query.assert_called_once_with(Topic)
            order_by_mock.offset.assert_called_once_with(self.filter_params.offset)
            offset_mock.limit.assert_called_once_with(self.filter_params.limit)

    def test_get_all_returnsNoTopics_userNotAdmin_noPermissions_userNotAuthor(self):
        self.topic.category_id = self.category.id
        self.topic2.category_id = self.category2.id

        self.user.permissions = []

        query_mock = self.db.query.return_value
        join_mock = query_mock.join.return_value
        filter_mock = join_mock.filter.return_value
        order_by_mock = filter_mock.order_by.return_value
        offset_mock = order_by_mock.offset.return_value
        limit_mock = offset_mock.limit.return_value
        limit_mock.all.return_value = []

        expected = []

        with (
            patch(
                "forum_system_api.services.topic_service.is_admin", return_value=False
            ),
            patch(
                "forum_system_api.services.topic_service.getattr",
                return_value=Topic.created_at,
            ),
        ):
            topics = topic_service.get_all(self.filter_params, self.user, self.db)

            self.assertEqual(topics, expected)
            self.db.query.assert_called_once_with(Topic)
            order_by_mock.offset.assert_called_once_with(self.filter_params.offset)
            offset_mock.limit.assert_called_once_with(self.filter_params.limit)

    def test_get_all_returnsTopics_userNotAdmin_noPermissions_userIsAuthor(self):
        self.topic.category_id = self.category.id
        self.topic.author_id = self.user.id
        self.topic2.category_id = self.category2.id

        self.user.permissions = []

        query_mock = self.db.query.return_value
        join_mock = query_mock.join.return_value
        filter_mock = join_mock.filter.return_value
        order_by_mock = filter_mock.order_by.return_value
        offset_mock = order_by_mock.offset.return_value
        limit_mock = offset_mock.limit.return_value
        limit_mock.all.return_value = [self.topic]

        expected = [self.topic]

        with (
            patch(
                "forum_system_api.services.topic_service.is_admin", return_value=False
            ),
            patch(
                "forum_system_api.services.topic_service.getattr",
                return_value=Topic.created_at,
            ),
        ):
            topics = topic_service.get_all(self.filter_params, self.user, self.db)

            self.assertEqual(topics, expected)
            self.db.query.assert_called_once_with(Topic)

    def test_get_public_returnsPublicTopics(self):
        query_mock = self.db.query.return_value
        join_mock = query_mock.join.return_value
        filter_mock = join_mock.filter.return_value
        order_by_mock = filter_mock.order_by.return_value
        offset_mock = order_by_mock.offset.return_value
        limit_mock = offset_mock.limit.return_value
        limit_mock.all.return_value = [self.topic]

        topics = topic_service.get_public(self.filter_params, self.db)

        self.assertEqual(topics, [self.topic])

        self.db.query.assert_called_once_with(Topic)
        order_by_mock.offset.assert_called_once_with(self.filter_params.offset)
        offset_mock.limit.assert_called_once_with(self.filter_params.limit)

    def test_get_public_returnsNoTopics_private(self):
        query_mock = self.db.query.return_value
        join_mock = query_mock.join.return_value
        filter_mock = join_mock.filter.return_value
        order_by_mock = filter_mock.order_by.return_value
        offset_mock = order_by_mock.offset.return_value
        limit_mock = offset_mock.limit.return_value
        limit_mock.all.return_value = []

        topics = topic_service.get_public(self.filter_params, self.db)

        self.assertEqual(topics, [])

        self.db.query.assert_called_once_with(Topic)
        join_mock.filter.assert_called_once()
        order_by_mock.offset.assert_called_once_with(self.filter_params.offset)
        limit_mock.all.assert_called_once()
        offset_mock.limit.assert_called_once_with(self.filter_params.limit)

    def test_get_by_id_returnsTopic_userIsAdmin(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.topic

        with (
            patch(
                "forum_system_api.services.topic_service.is_admin", return_value=True
            ),
            patch(
                "forum_system_api.services.topic_service.verify_topic_permission",
                return_value=None,
            ),
        ):
            topic = topic_service.get_by_id(self.topic.id, self.user, self.db)

            self.assertEqual(topic, self.topic)

            self.db.query.assert_called_once_with(Topic)
            assert_filter_called_with(query_mock, Topic.id == self.topic.id)

    def test_get_by_id_returnsNoTopic_userNotAdmin_noPermissions(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.topic

        with (
            patch(
                "forum_system_api.services.topic_service.is_admin", return_value=False
            ),
            patch(
                "forum_system_api.services.topic_service.verify_topic_permission",
                return_value=None,
            ),
        ):
            topic = topic_service.get_by_id(self.topic.id, self.user, self.db)

            self.assertEqual(topic, self.topic)

            self.db.query.assert_called_once_with(Topic)
            assert_filter_called_with(query_mock, Topic.id == self.topic.id)

    def test_get_by_id_noTopic_returns404(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None

        with self.assertRaises(HTTPException) as context:
            topic_service.get_by_id(self.topic.id, self.user, self.db)

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, "Topic not found")

        self.db.query.assert_called_once_with(Topic)
        assert_filter_called_with(query_mock, Topic.id == self.topic.id)

    def test_get_by_title_returnsTopic(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.topic

        topic = topic_service.get_by_title(self.topic.title, self.db)

        self.assertEqual(topic, self.topic)

        self.db.query.assert_called_once_with(Topic)
        assert_filter_called_with(query_mock, Topic.title == self.topic.title)
        filter_mock.first.assert_called_once()

    def test_get_by_title_noTopic_returnsNone(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None

        topic = topic_service.get_by_title("Mock title", self.db)

        self.assertIsNone(topic)

        self.db.query.assert_called_once_with(Topic)
        assert_filter_called_with(query_mock, Topic.title == "Mock title")

    def test_create_topic_createsTopic(self):
        topic_create = TopicCreate(
            title=td.VALID_TOPIC_TITLE_2, content=td.VALID_TOPIC_CONTENT_2
        )
        topic2 = Topic(**tobj.VALID_TOPIC_2)

        with (
            patch(
                "forum_system_api.services.topic_service.user_permission",
                return_value=True,
            ),
            patch(
                "forum_system_api.services.topic_service.get_by_title",
                return_value=None,
            ),
        ):
            new_topic = topic_service.create(
                topic2.category_id, topic_create, self.user, self.db
            )

            self.db.add.assert_called_once()
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(new_topic)
            self.assertEqual(new_topic.author_id, self.user.id)
            self.assertEqual(new_topic.title, topic2.title)
            self.assertEqual(new_topic.content, topic2.content)
            self.assertEqual(new_topic.category_id, topic2.category_id)

    def test_create_topic_raises403_noUserPermission(self):
        topic_create = TopicCreate(
            title=td.VALID_TOPIC_TITLE_2, content=td.VALID_TOPIC_CONTENT_2
        )
        with patch(
            "forum_system_api.services.topic_service.user_permission",
            return_value=False,
        ):
            with self.assertRaises(HTTPException) as context:
                topic_service.create(
                    self.topic.category_id, topic_create, self.user, self.db
                )

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(
                context.exception.detail,
                "You don't have permission to post in this category",
            )

            self.db.add.assert_not_called()
            self.db.commit.assert_not_called()
            self.db.refresh.assert_not_called()

    def test_create_topic_raises409_topicExists(self):
        topic_create = TopicCreate(
            title=td.VALID_TOPIC_TITLE_2, content=td.VALID_TOPIC_CONTENT_2
        )
        with (
            patch(
                "forum_system_api.services.topic_service.user_permission",
                return_value=True,
            ),
            patch(
                "forum_system_api.services.topic_service.get_by_title",
                return_value=self.topic,
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                topic_service.create(
                    self.topic.category_id, topic_create, self.user, self.db
                )

            self.assertEqual(context.exception.status_code, status.HTTP_409_CONFLICT)
            self.assertEqual(
                context.exception.detail,
                "Topic with this title already exists, please select a new title",
            )

            self.db.add.assert_not_called()
            self.db.commit.assert_not_called()
            self.db.refresh.assert_not_called

    def test_update_topic_updatesTopic_updateParams(self):
        update_topic = TopicUpdate(
            title=td.VALID_TOPIC_TITLE_2,
            content=td.VALID_TOPIC_CONTENT_2,
            category_id=td.VALID_TOPIC_CATEGORY_ID_2,
        )
        with (
            patch(
                "forum_system_api.services.topic_service._validate_topic_access",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.topic_service.user_permission",
                return_value=True,
            ),
        ):
            updated_topic = topic_service.update(
                self.user, self.topic.id, update_topic, self.db
            )

            self.assertEqual(updated_topic, self.topic)
            self.assertEqual(updated_topic.title, td.VALID_TOPIC_TITLE_2)
            self.assertEqual(updated_topic.content, td.VALID_TOPIC_CONTENT_2)
            self.assertEqual(updated_topic.category_id, td.VALID_TOPIC_CATEGORY_ID_2)

            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(self.topic)

    def test_update_topic_noUpdate_noParams(self):
        update_topic = TopicUpdate(title=None, content=None, category_id=None)
        with (
            patch(
                "forum_system_api.services.topic_service._validate_topic_access",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.topic_service.user_permission",
                return_value=True,
            ),
        ):
            updated_topic = topic_service.update(
                self.user, self.topic.id, update_topic, self.db
            )

            self.assertEqual(updated_topic, self.topic)
            self.assertEqual(updated_topic.title, td.VALID_TOPIC_TITLE_1)
            self.assertEqual(updated_topic.content, td.VALID_TOPIC_CONTENT_1)
            self.assertEqual(updated_topic.category_id, td.VALID_TOPIC_CATEGORY_ID_1)

            self.db.commit.assert_not_called()
            self.db.refresh.assert_not_called()

    def test_update_topic_raises403_noUserPermission(self):
        update_topic = TopicUpdate(
            title=td.VALID_TOPIC_TITLE_2,
            content=td.VALID_TOPIC_CONTENT_2,
            category_id=td.VALID_TOPIC_CATEGORY_ID_2,
        )
        with (
            patch(
                "forum_system_api.services.topic_service._validate_topic_access",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.topic_service.user_permission",
                return_value=False,
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                topic_service.update(self.user, self.topic.id, update_topic, self.db)

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(
                context.exception.detail, "You don't have permission to do that"
            )

            self.db.commit.assert_not_called()
            self.db.refresh.assert_not_called()

    def test_get_replies_returnsReplies_replies(self):
        query_mock = self.db.query.return_value
        options_mock = query_mock.options.return_value
        filter_mock = options_mock.filter.return_value
        order_by_mock = filter_mock.order_by.return_value
        order_by_mock.all.return_value = [self.reply]

        self.topic.replies = [self.reply]

        replies = topic_service.get_replies(self.topic.id, self.db)

        self.assertEqual(replies, self.topic.replies)

        self.db.query.assert_called_once_with(Reply)
        assert_filter_called_with(options_mock, Reply.topic_id == self.topic.id)
        query_mock.options.assert_called_once()

    def test_get_replies_returnsEmptyList_noReplies(self):
        query_mock = self.db.query.return_value
        options_mock = query_mock.options.return_value
        filter_mock = options_mock.filter.return_value
        order_by_mock = filter_mock.order_by.return_value
        order_by_mock.all.return_value = []

        self.topic.replies = []

        replies = topic_service.get_replies(self.topic.id, self.db)

        self.assertEqual(replies, self.topic.replies)

        self.db.query.assert_called_once_with(Reply)
        assert_filter_called_with(options_mock, Reply.topic_id == self.topic.id)
        query_mock.options.assert_called_once()

    def test_lock_updatesTopic(self):
        topic_lock = td.VALID_TOPIC_IS_LOCKED_2

        with patch(
            "forum_system_api.services.topic_service.get_by_id", return_value=self.topic
        ):
            topic = topic_service.lock(self.user, self.topic.id, topic_lock, self.db)

            self.assertEqual(topic.is_locked, self.topic.is_locked)
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(self.topic)

    def test_select_best_reply_updatesTopic(self):
        self.topic.best_reply_id = self.reply.id

        with (
            patch(
                "forum_system_api.services.topic_service._validate_topic_access",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.topic_service.get_reply_by_id",
                return_value=self.reply,
            ),
        ):
            topic = topic_service.select_best_reply(
                self.user, self.topic.id, self.reply.id, self.db
            )

            self.assertEqual(self.reply.id, topic.best_reply_id)
            self.db.commit.assert_called_once()
            self.db.refresh.assert_called_once_with(self.topic)

    def test_get_topics_for_category_returnsTopics(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.all.return_value = [self.topic]

        with patch(
            "forum_system_api.services.category_service.get_by_id",
            return_value=self.category,
        ):
            topics = topic_service.get_topics_for_category(
                self.category.id, self.user, self.db
            )

        self.assertEqual(topics, [self.topic])

        self.db.query.assert_called_once_with(Topic)
        assert_filter_called_with(query_mock, Topic.category_id == self.category.id)
        filter_mock.all.assert_called_once()

    def test_get_topics_for_category_raises404_noCategory(self):
        with patch(
            "forum_system_api.services.category_service.get_by_id",
            return_value=None,
        ):
            with self.assertRaises(HTTPException) as context:
                topic_service.get_topics_for_category(
                    self.category.id, self.user, self.db
                )

        self.assertEqual(context.exception.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(context.exception.detail, "Category not found")

    def test_get_topics_for_category_raises403_noPermissions(self):
        with (
            patch(
                "forum_system_api.services.category_service.get_by_id",
                return_value=self.category2,
            ),
            patch(
                "forum_system_api.services.topic_service.is_admin",
                return_value=False,
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                topic_service.get_topics_for_category(
                    self.category.id, self.user, self.db
                )

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(context.exception.detail, "Unauthorized")

    def test_validate_topic_access_returnsTopic_userIsAdmin(self):
        with (
            patch(
                "forum_system_api.services.topic_service.get_by_id",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.topic_service.is_admin", return_value=True
            ),
        ):
            topic = topic_service._validate_topic_access(
                self.topic.id, self.user, self.db
            )

            self.assertEqual(topic, self.topic)

    def test_validate_topic_access_raises403_userNotAuthor_userNotAdmin(self):
        self.topic.author_id = td.VALID_USER_ID_2
        with (
            patch(
                "forum_system_api.services.topic_service.get_by_id",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.topic_service.is_admin", return_value=False
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                topic_service._validate_topic_access(self.topic.id, self.user, self.db)

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(context.exception.detail, "Unauthorized")

    def test_validate_topic_access_raises403_userIsAuthor_topicLocked(self):
        self.topic.author_id = self.user.id
        self.topic.is_locked = td.VALID_TOPIC_IS_LOCKED_1
        with (
            patch(
                "forum_system_api.services.topic_service.get_by_id",
                return_value=self.topic,
            ),
            patch(
                "forum_system_api.services.topic_service.is_admin", return_value=False
            ),
        ):
            with self.assertRaises(HTTPException) as context:
                topic_service._validate_topic_access(self.topic.id, self.user, self.db)

            self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(context.exception.detail, "Topic is locked")
