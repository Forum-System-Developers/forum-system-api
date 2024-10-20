import unittest
from unittest.mock import MagicMock, patch, Mock, ANY
from sqlalchemy.orm import Session

from fastapi import HTTPException

from tests.services import test_data_const as td
from tests.services import test_data_obj as tobj
from forum_system_api.schemas.common import TopicFilterParams
from forum_system_api.persistence.models.user import User
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.category import Category
from forum_system_api.services import topic_service
from tests.services.utils import assert_filter_called_with
from forum_system_api.persistence.models.user_category_permission import UserCategoryPermission
from forum_system_api.services.user_service import is_admin


class TopicServiceShould(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = User(**tobj.USER_1)
        self.topic1 = Topic(**tobj.VALID_TOPIC_1)
        self.topic2 = Topic(**tobj.VALID_TOPIC_2)
        self.category = Category(**tobj.VALID_CATEGORY_1)
        self.filter_params = TopicFilterParams(**tobj.VALID_TOPIC_FILTER_PARAMS)
       
    
    def test_getAll_returnsTopics(self):
        query_mock = self.db.query.return_value
        join_mock = query_mock.join.return_value
        filter_mock = join_mock.filter.return_value
        filter_mock.all.return_value = [self.topic1, self.topic2]
        
        topics = topic_service.get_all(self.filter_params, self.user, self.db)
        
        self.assertEqual(topics, [self.topic1, self.topic2])
        
        self.db.query.assert_called_once_with(Topic)
        query_mock.join.assert_called_once_with(Category, Topic.category_id == Category.id)
        assert_filter_called_with(filter_mock, ANY)
        
        
    def test_getAll_noTopics_returnsEmptyList(self):
        query_mock = self.db.query.return_value
        join_mock = query_mock.join.return_value
        filter_mock = join_mock.filter.return_value
        filter_mock.filter.return_value = []
        
        topics = topic_service.get_all(self.filter_params, self.user, self.db)
        
        self.assertEqual(topics, [])
        
        self.db.query.assert_called_once_with(Topic)
        query_mock.join.assert_called_once_with(Category, Topic.category_id == Category.id)
        assert_filter_called_with(filter_mock, ANY)
        
    
    def test_getAll_userPermission_returnsTopics(self):
        query_mock = self.db.query.return_value
        join_mock = query_mock.join.return_value
        filter_mock = join_mock.filter.return_value
        filter_mock.filter.return_value = [self.topic1, self.topic2]
        
        topics = topic_service.get_all(self.filter_params, self.user, self.db)
        
        self.assertEqual(topics, [self.topic1, self.topic2])
        
        self.db.query.assert_called_once_with(Topic)
        query_mock.join.assert_called_once_with(Category, Topic.category_id == Category.id)
        assert_filter_called_with(filter_mock, ANY)
        
        
    def test_getAll_userIsAdmin_returnsTopics(self):
        query_mock = self.db.query.return_value
        join_mock = query_mock.join.return_value
        filter_mock = join_mock.filter.return_value
        filter_mock.filter.return_value = [self.topic1, self.topic2]
        
        topics = topic_service.get_all(self.filter_params, self.user, self.db)
        
        self.assertEqual(topics, [self.topic1, self.topic2])
        
        self.db.query.assert_called_once_with(Topic)
        query_mock.join.assert_called_once_with(Category, Topic.category_id == Category.id)
        assert_filter_called_with(filter_mock, ANY)
    

    def test_getById_returnsTopic(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.topic1
        
        topic = topic_service.get_by_id(self.topic1.id, self.user, self.db)
        
        self.assertEqual(topic, self.topic1)
        
        self.db.query.assert_called_once_with(Topic)
        assert_filter_called_with(query_mock, Topic.id == self.topic1.id)
    
    
    def test_getById_topicNotFound_raises404(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None
        
        with self.assertRaises(HTTPException) as context:
            topic_service.get_by_id(self.topic1.id, self.user, self.db)
        
        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Topic not found")
        
        self.db.query.assert_called_once_with(Topic)
        assert_filter_called_with(query_mock, Topic.id == self.topic1.id)
        
    def test_getByTitle_returnsTopic(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = self.topic1
        
        topic = topic_service.get_by_title(self.topic1.title, self.user, self.db)
        
        self.assertEqual(topic, self.topic1)
        
        self.db.query.assert_called_once_with(Topic)
        assert_filter_called_with(query_mock, Topic.title == self.topic1.title)
        
    def test_getByName_topicNotFound_returnsNone(self):
        query_mock = self.db.query.return_value
        filter_mock = query_mock.filter.return_value
        filter_mock.first.return_value = None
        
        topic = topic_service.get_by_title(self.topic1.title, self.user, self.db)
        
        self.assertIsNone(topic)
        
        self.db.query.assert_called_once_with(Topic)
        assert_filter_called_with(query_mock, Topic.title == self.topic1.title)
