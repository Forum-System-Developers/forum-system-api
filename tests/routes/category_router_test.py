import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.user import User
from forum_system_api.services.auth_service import require_admin_role
from forum_system_api.api.api_v1.constants import endpoints as e
from tests.services import test_data as td
from tests.services.test_data_obj import USER_1

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
