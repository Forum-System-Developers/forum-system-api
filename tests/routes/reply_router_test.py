import unittest
import uuid
from unittest.mock import MagicMock, patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from forum_system_api.main import app
from forum_system_api.persistence.database import get_db
from forum_system_api.persistence.models.reply import Reply
from forum_system_api.persistence.models.topic import Topic
from forum_system_api.persistence.models.user import User
from forum_system_api.services.auth_service import get_current_user
from tests.services import test_data_obj as tobj


class ReplyRouterShould(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db = MagicMock()
        self.user = User(**tobj.USER_1)
        self.topic = Topic(**tobj.VALID_TOPIC_1)
        self.topic.author = self.user
        self.reply = Reply(**tobj.VALID_REPLY)
        self.reply.author = self.user

    def tearDown(self) -> None:
        app.dependency_overrides = {}

    def test_get_by_id_returns200_onSuccess(self):
        with (
            patch(
                "forum_system_api.services.reply_service.get_by_id",
                return_value=self.reply,
            ),
            patch(
                "forum_system_api.services.reply_service.get_votes", return_value=(1, 0)
            ),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.get(f"/api/v1/replies/{self.reply.id}")

            self.assertEqual(response.status_code, 200)

    def test_get_by_id_returns404_replyNotFound(self):
        with patch(
            "forum_system_api.services.reply_service.get_by_id",
            side_effect=HTTPException(status_code=404, detail="Reply not found"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.get(f"/api/v1/replies/{uuid.uuid4()}")

            self.assertEqual(response.status_code, 404)
            self.assertIn("Reply not found", response.json()["detail"])

    def test_get_by_id_returns403_noTopicPermissions(self):
        with patch(
            "forum_system_api.services.reply_service.get_by_id",
            side_effect=HTTPException(status_code=403, detail="Unauthorized"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.get(f"/api/v1/replies/{self.topic.id}")

            self.assertEqual(response.status_code, 403)
            self.assertIn("Unauthorized", response.json()["detail"])

    def test_create_returns_201_onSuccess(self):
        with patch(
            "forum_system_api.services.reply_service.create", return_value=self.reply
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.post(
                f"/api/v1/replies/{self.topic.id}", json=tobj.VALID_REPLY_CREATE
            )

            self.assertEqual(response.status_code, 201)

    def test_create_returns_403_noPermissions(self):
        with patch(
            "forum_system_api.services.reply_service.create",
            side_effect=HTTPException(status_code=403, detail="Unauthorized"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.post(
                f"/api/v1/replies/{self.topic.id}", json=tobj.VALID_REPLY_CREATE
            )

            self.assertEqual(response.status_code, 403)

    def test_update_returns_200_onSuccess(self):
        with (
            patch(
                "forum_system_api.services.reply_service.update",
                return_value=self.reply,
            ),
            patch(
                "forum_system_api.services.reply_service.get_votes", return_value=(1, 0)
            ),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.put(
                f"/api/v1/replies/{self.reply.id}", json=tobj.VALID_REPLY_CREATE
            )

            self.assertEqual(response.status_code, 200)

    def test_update_returns_403_noPermissions(self):
        with patch(
            "forum_system_api.services.reply_service.update",
            side_effect=HTTPException(status_code=403, detail="Cannot update reply"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.put(
                f"/api/v1/replies/{self.reply.id}", json=tobj.VALID_REPLY_CREATE
            )

            self.assertEqual(response.status_code, 403)
            self.assertIn("Cannot update reply", response.json()["detail"])

    def test_update_returns_404_replyNotFound(self):
        with patch(
            "forum_system_api.services.reply_service.update",
            side_effect=HTTPException(status_code=404, detail="Reply not found"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.put(
                f"/api/v1/replies/{self.reply.id}", json=tobj.VALID_REPLY_CREATE
            )

            self.assertEqual(response.status_code, 404)
            self.assertIn("Reply not found", response.json()["detail"])

    def test_create_reaction_returns_200_onSuccess(self):
        with (
            patch(
                "forum_system_api.services.reply_service.vote", return_value=self.reply
            ),
            patch(
                "forum_system_api.services.reply_service.get_votes", return_value=(1, 0)
            ),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.patch(
                f"/api/v1/replies/{self.reply.id}",
                json=tobj.VALID_REPLY_REACTION_CREATE_TRUE,
            )

            self.assertEqual(response.status_code, 200)

    def test_create_reaction_returns_404_replyNotFound(self):
        with patch(
            "forum_system_api.services.reply_service.vote",
            side_effect=HTTPException(status_code=404, detail="Reply not found"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.patch(
                f"/api/v1/replies/{self.reply.id}",
                json=tobj.VALID_REPLY_REACTION_CREATE_TRUE,
            )

            self.assertEqual(response.status_code, 404)
            self.assertIn("Reply not found", response.json()["detail"])

    def test_create_reaction_returns_405_noPermissions(self):
        with patch(
            "forum_system_api.services.reply_service.vote",
            side_effect=HTTPException(status_code=405, detail="Unauthorized"),
        ):
            app.dependency_overrides[get_db] = lambda: self.db
            app.dependency_overrides[get_current_user] = lambda: self.user

            response = self.client.patch(
                f"/api/v1/replies/{self.reply.id}",
                json=tobj.VALID_REPLY_REACTION_CREATE_TRUE,
            )

            self.assertEqual(response.status_code, 405)
            self.assertIn("Unauthorized", response.json()["detail"])
