import unittest
from unittest.mock import MagicMock
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session

from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.schemas.common import FilterParams
from forum_system_api.schemas.topic import TopicCreate, TopicLock, TopicUpdate
from forum_system_api.services import topic_service


class TestTopicService(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user_id = uuid4()
        self.topic_id = uuid4()
        self.category_id = uuid4()

    def test_get_all(self):
        filter_params = FilterParams(order="asc", order_by="title", offset=0, limit=10)

        self.db.query.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = [
            Topic(id=self.topic_id, title="Test Topic", category_id=self.category_id)
        ]

        topics = topic_service.get_all(filter_params, self.db)

        self.assertEqual(len(topics), 1)
        self.assertEqual(topics[0].title, "Test Topic")

    def test_get_by_id_success(self):
        # Mock the return value for a valid topic
        self.db.query.return_value.filter.return_value.first.return_value = Topic(
            id=self.topic_id
        )

        # Call the service function
        topic = topic_service.get_by_id(self.topic_id, self.db)

        # Assert the returned topic
        self.assertEqual(topic.id, self.topic_id)

    def test_get_by_id_not_found(self):
        # Mock return value for topic not found
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Expect an HTTPException to be raised
        with self.assertRaises(HTTPException) as context:
            get_by_id(self.topic_id, self.db)

        # Assert the exception status code
        self.assertEqual(context.exception.status_code, 404)

    def test_create_success(self):
        # Prepare a TopicCreate object
        topic_create = TopicCreate(title="New Topic", category_id=self.category_id)
        # Mock return value for category lookup
        self.db.query.return_value.filter.return_value.first.return_value = (
            None  # Assume category exists
        )

        # Mock Topic creation
        new_topic = Topic(
            id=self.topic_id,
            title="New Topic",
            category_id=self.category_id,
            author_id=self.user_id,
        )
        self.db.add.return_value = None  # Add method doesn't return anything

        # Call the create function
        created_topic = create(topic_create, self.user_id, self.db)

        # Assert the returned topic matches what was created
        self.assertEqual(created_topic.title, "New Topic")
        self.assertEqual(created_topic.author_id, self.user_id)

    def test_create_category_not_found(self):
        # Prepare a TopicCreate object
        topic_create = TopicCreate(title="New Topic", category_id=self.category_id)
        # Mock return value for category lookup to simulate category not found
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Expect an HTTPException to be raised
        with self.assertRaises(HTTPException) as context:
            create(topic_create, self.user_id, self.db)

        # Assert the exception status code
        self.assertEqual(context.exception.status_code, 404)

    def test_update_success(self):
        # Mock existing topic
        existing_topic = Topic(
            id=self.topic_id, author_id=self.user_id, title="Old Title"
        )
        self.db.query.return_value.filter.return_value.first.return_value = (
            existing_topic
        )

        # Prepare an update request
        updated_topic = TopicUpdate(title="Updated Title", category_id=self.category_id)
        # Mock reply and category lookup
        self.db.query.return_value.filter.return_value.first.return_value = Reply(
            id=uuid4()
        )  # Assume valid reply
        self.db.query.return_value.filter.return_value.first.return_value = Topic(
            id=self.category_id
        )  # Assume valid category

        # Call the update function
        updated = update(User(id=self.user_id), self.topic_id, updated_topic, self.db)

        # Assert the updated topic matches expected values
        self.assertEqual(updated.title, "Updated Title")

    def test_update_topic_not_found(self):
        # Mock to simulate topic not found
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Expect an HTTPException to be raised
        with self.assertRaises(HTTPException) as context:
            update(
                User(id=self.user_id),
                self.topic_id,
                TopicUpdate(title="Updated Title", category_id=self.category_id),
                self.db,
            )

        # Assert the exception status code
        self.assertEqual(context.exception.status_code, 404)

    def test_lock_success(self):
        # Mock existing topic
        topic = Topic(id=self.topic_id, is_locked=False)
        self.db.query.return_value.filter.return_value.first.return_value = topic

        # Prepare lock data
        lock_data = TopicLock(is_locked=True)

        # Call the lock function
        updated_topic = lock(self.topic_id, lock_data, self.db)

        # Assert that the topic is now locked
        self.assertTrue(updated_topic.is_locked)

    def test_select_best_reply_success(self):
        # Mock existing topic
        topic = Topic(id=self.topic_id, author_id=self.user_id)
        reply_id = uuid4()
        self.db.query.return_value.filter.return_value.first.return_value = topic
        self.db.query.return_value.filter.return_value.first.return_value = Reply(
            id=reply_id
        )

        # Call the select_best_reply function
        updated_topic = select_best_reply(
            User(id=self.user_id), self.topic_id, reply_id, self.db
        )

        # Assert that the best reply ID has been set
        self.assertEqual(updated_topic.best_reply_id, reply_id)

    def test_select_best_reply_unauthorized(self):
        # Mock existing topic with a different author
        topic = Topic(id=self.topic_id, author_id=uuid4())  # Different author
        self.db.query.return_value.filter.return_value.first.return_value = topic

        # Expect an HTTPException to be raised
        with self.assertRaises(HTTPException) as context:
            select_best_reply(User(id=self.user_id), self.topic_id, uuid4(), self.db)

        # Assert the exception status code
        self.assertEqual(context.exception.status_code, 403)

    def test_select_best_reply_not_found(self):
        # Mock to simulate topic not found
        self.db.query.return_value.filter.return_value.first.return_value = None

        # Expect an HTTPException to be raised
        with self.assertRaises(HTTPException) as context:
            select_best_reply(User(id=self.user_id), self.topic_id, uuid4(), self.db)

        # Assert the exception status code
        self.assertEqual(context.exception.status_code, 404)
