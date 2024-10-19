import unittest
from unittest.mock import MagicMock, patch, Mock
from uuid import UUID
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


class TopicServiceShould(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.user = Mock(spec=User)


    def test_get_all_topics(self):
        topic1 = Mock(spec=Topic)
        topic2 = Mock(spec=Topic)
        user = Mock(spec=User)
        mock_topics = [topic1, topic2]
        filter_params = Mock(spec=TopicFilterParams)        

        self.db.query.return_value.all.return_value = mock_topics
        

        topics = topic_service.get_all(filter_params, user, self.db)
        

        self.db.query.assert_called_once_with(Topic) 
        
        self.assertEqual(topics, mock_topics)