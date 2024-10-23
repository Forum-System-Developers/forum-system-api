import unittest
import uuid
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.services.auth_service import get_current_user
from tests.services import test_data_obj as tobj


class TopicRouterShould(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = MagicMock()
        self.user = User(**tobj.USER_1)
        self.topic = Topic(**tobj.VALID_TOPIC_1)

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    def test_get_all_returns200_onSuccess(self):
        with patch(
            "forum_system_api.services.topic_service.get_all", return_value=[self.topic]
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.get("/api/v1/topics/")

            self.assertEqual(response.status_code, 200)

    def test_get_by_id_returns200_onSuccess(self):
        with patch(
            "forum_system_api.services.topic_service.get_by_id", return_value=self.topic
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.get(f"/api/v1/topics/{self.topic.id}")

            self.assertEqual(response.status_code, 200)

    def test_get_by_id_returns404_topicNotFound(self):
        with patch(
            "forum_system_api.services.topic_service.get_by_id",
            side_effect=HTTPException(status_code=404, detail="Topic not found"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.get(f"/api/v1/topics/{uuid.uuid4()}")

            self.assertEqual(response.status_code, 404)
            self.assertIn("Topic not found", response.json()["detail"])

    def test_get_by_id_returns403_noTopicPermissions(self):
        with patch(
            "forum_system_api.services.topic_service.get_by_id",
            side_effect=HTTPException(status_code=403, detail="Unauthorized"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.get(f"/api/v1/topics/{self.topic.id}")

            self.assertEqual(response.status_code, 403)
            self.assertIn("Unauthorized", response.json()["detail"])

    def test_create_returns_201_onSuccess(self):
        with patch(
            "forum_system_api.services.topic_service.create", return_value=self.topic
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.post("/api/v1/topics/", json=tobj.VALID_TOPIC_CREATE)

            self.assertEqual(response.status_code, 201)

    def test_create_returns_403_noPermissions(self):
        with patch(
            "forum_system_api.services.topic_service.create",
            side_effect=HTTPException(status_code=403, detail="Unauthorized"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.post("/api/v1/topics/", json=tobj.VALID_TOPIC_CREATE)

            self.assertEqual(response.status_code, 403)

    def test_update_returns_200_onSuccess(self):
        with patch(
            "forum_system_api.services.topic_service.update", return_value=self.topic
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.put(
                f"/api/v1/topics/{self.topic.id}", json=tobj.VALID_TOPIC_CREATE
            )

            self.assertEqual(response.status_code, 200)

    def test_update_returns_403_noPermissions(self):
        with patch(
            "forum_system_api.services.topic_service.update",
            side_effect=HTTPException(status_code=403, detail="Unauthorized"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.put(
                f"/api/v1/topics/{self.topic.id}", json=tobj.VALID_TOPIC_CREATE
            )

            self.assertEqual(response.status_code, 403)
            self.assertIn("Unauthorized", response.json()["detail"])

    def test_update_returns_404_topicNotFound(self):
        with patch(
            "forum_system_api.services.topic_service.update",
            side_effect=HTTPException(status_code=404, detail="Topic not found"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.put(
                f"/api/v1/topics/{self.topic.id}", json=tobj.VALID_TOPIC_CREATE
            )

            self.assertEqual(response.status_code, 404)
            self.assertIn("Topic not found", response.json()["detail"])

    def test_lock_returns_200_onSuccess(self):
        with patch(
            "forum_system_api.services.topic_service.lock", return_value=self.topic
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.put(
                f"/api/v1/topics/{self.topic.id}/locked", json=True
            )

            self.assertEqual(response.status_code, 200)

    def test_best_reply_returns_200_onSuccess(self):
        with patch(
            "forum_system_api.services.topic_service.select_best_reply",
            return_value=self.topic,
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.put(
                f"/api/v1/topics/{self.topic.id}/replies/{self.reply.id}/best"
            )

            self.assertEqual(response.status_code, 200)
