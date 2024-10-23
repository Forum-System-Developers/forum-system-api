import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.services.auth_service import get_current_user, require_admin_role
from forum_system_api.api.api_v1.constants import endpoints as e
from tests.services import test_data as td
from tests.services.test_data_obj import USER_1, VALID_REPLY, VALID_TOPIC_1

client = TestClient(app)

class TestCategoryRouter_Should(unittest.TestCase):
    
    def setUp(self) -> None:
        self.mock_db = MagicMock(spec=Session)
        self.mock_admin = MagicMock(spec=User)
        self.user = User(**USER_1)

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    @patch('forum_system_api.services.category_service.create_category')
    def test_create_category_returns201_onSuccess(self, mock_create_category) -> None:
        # Arrange
        mock_create_category.return_value = td.CATEGORY_1
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        app.dependency_overrides[get_db] = lambda: self.mock_db
        
        # Act
        response = client.post(e.CATEGORY_ENDPOINT_CREATE_CATEGORY, json=td.CATEGORY_CREATE)
        
        # Assert
        self.assertEqual(response.status_code, 201)

    @patch('forum_system_api.services.category_service.get_all')
    def test_get_categories_returns200_onSuccess(self, mock_get_all) -> None:
        # Arrange
        app.dependency_overrides[get_db] = lambda: self.mock_db
        mock_get_all.return_value = [td.CATEGORY_1, td.CATEGORY_2]
        
        # Act
        response = client.get(e.CATEGORY_ENDPOINT_GET_CATEGORIES)
        
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    @patch('forum_system_api.services.topic_service.get_all')
    @patch('forum_system_api.services.topic_service.get_replies')
    def test_view_category_returns200_onSuccess(self, mock_get_replies, mock_get_all) -> None:
        # Arrange
        topic_instance = Topic(id=VALID_TOPIC_1["id"], category_id=VALID_TOPIC_1["category_id"])
        mock_get_all.return_value = [topic_instance]
        mock_get_replies.return_value = [VALID_REPLY]
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[get_current_user] = lambda: self.user

        # Act
        response = client.get(e.CATEGORY_ENDPOINT_VIEW_CATEGORY.format(td.VALID_CATEGORY_ID))
        
        # Assert
        self.assertEqual(response.status_code, 200)
