# import unittest
# from datetime import datetime
# from unittest.mock import MagicMock, patch

# from sqlalchemy.orm import Session
# from fastapi.testclient import TestClient

# from forum_system_api.schemas.user import UserResponse
# from forum_system_api.main import app


# client = TestClient(app)

# class TestUserRouter_Should(unittest.TestCase):
#     def setUp(self):
#         self.mock_db = MagicMock(spec=Session)

#     @patch("forum_system_api.services.user_service.create")
#     @patch("forum_system_api.persistence.database.get_db")
#     def test_registerUser_success(self, mock_get_db, mock_create):
#         # Arrange
#         mock_get_db.return_value = self.mock_db
#         mock_create.return_value = UserResponse(
#             username="newuser", 
#             first_name="New", 
#             last_name="User", 
#             email="newuser@example.com",
#             created_at=datetime.now()
#         )

#         user_data = {
#             "username": "newuser",
#             "email": "newuser@example.com",
#             "password": "securepassword",
#             "first_name": "New",
#             "last_name": "User"
#         }

#         # Act
#         response = client.post("/api/v1/users/register", json=user_data)
        
#         # Assert
#         self.assertEqual(response.status_code, 200)
#         data = response.json()
#         self.assertEqual(data["username"], "newuser")
#         self.assertEqual(data["email"], "newuser@example.com")
#         self.assertEqual(data["first_name"], "New")
#         self.assertEqual(data["last_name"], "User")
