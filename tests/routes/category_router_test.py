import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.services.auth_service import get_current_user, require_admin_role
from tests.services import test_data as td
from tests.services.test_data_obj import USER_1, VALID_REPLY, VALID_TOPIC_1

CATEGORY_ENDPOINT_CREATE_CATEGORY = "/api/v1/categories/"
CATEGORY_ENDPOINT_GET_CATEGORIES = "/api/v1/categories/"
CATEGORY_ENDPOINT_VIEW_CATEGORY = "/api/v1/categories/{}/topics/"
CATEGORY_PRIVACY_ENDPOINT = "/api/v1/categories/{}/private/"
CATEGORY_LOCK_ENDPOINT = "/api/v1/categories/{}/lock/"


client = TestClient(app)


class TestCategoryRouter_Should(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_db = MagicMock(spec=Session)
        self.mock_admin = MagicMock(spec=User)
        self.user = User(**USER_1)

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    @patch("forum_system_api.services.category_service.create_category")
    def test_create_category_returns201_onSuccess(self, mock_create_category) -> None:
        # Arrange
        mock_create_category.return_value = td.CATEGORY_1
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        response = client.post(
            CATEGORY_ENDPOINT_CREATE_CATEGORY, json=td.CATEGORY_CREATE
        )

        # Assert
        self.assertEqual(response.status_code, 201)

    @patch("forum_system_api.services.category_service.get_all")
    def test_get_categories_returns200_onSuccess(self, mock_get_all) -> None:
        # Arrange
        app.dependency_overrides[get_db] = lambda: self.mock_db
        mock_get_all.return_value = [td.CATEGORY_1, td.CATEGORY_2]

        # Act
        response = client.get(CATEGORY_ENDPOINT_GET_CATEGORIES)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)

    @patch("forum_system_api.services.topic_service.get_topics_for_category")
    @patch("forum_system_api.services.topic_service.get_replies")
    def test_view_category_returns200_onSuccess(
        self, mock_get_replies, mock_get_topics_for_category
    ) -> None:
        # Arrange
        topic = Topic(**VALID_TOPIC_1)
        topic.author = self.user
        reply = Reply(**VALID_REPLY)
        reply.author = self.user
        mock_get_topics_for_category.return_value = [topic]
        mock_get_replies.return_value = [reply]
        app.dependency_overrides[get_db] = lambda: self.mock_db
        app.dependency_overrides[get_current_user] = lambda: self.user

        # Act
        response = client.get(
            CATEGORY_ENDPOINT_VIEW_CATEGORY.format(td.VALID_CATEGORY_ID)
        )

        # Assert
        self.assertEqual(response.status_code, 200)

    @patch("forum_system_api.services.category_service.make_private_or_public")
    def test_make_category_private_or_public_returns200_onSuccess(
        self, mock_make_private_or_public
    ) -> None:
        # Arrange
        mock_make_private_or_public.return_value = td.CATEGORY_1
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin
        app.dependency_overrides[get_db] = lambda: self.mock_db

        # Act
        response = client.put(
            CATEGORY_PRIVACY_ENDPOINT.format(td.VALID_CATEGORY_ID),
            params={"is_private": True},
        )

        # Assert
        self.assertEqual(response.status_code, 200)

    @patch("forum_system_api.services.category_service.lock_or_unlock")
    def test_lock_or_unlock_category_returns200_onSuccess(
        self, mock_lock_or_unlock
    ) -> None:
        # Arrange
        mock_lock_or_unlock.return_value = td.CATEGORY_1
        app.dependency_overrides[require_admin_role] = lambda: self.mock_admin

        # Act
        response = client.put(
            CATEGORY_LOCK_ENDPOINT.format(td.VALID_CATEGORY_ID),
            params={"is_locked": True},
        )

        # Assert
        self.assertEqual(response.status_code, 200)
