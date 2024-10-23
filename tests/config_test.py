import unittest
from unittest.mock import patch

from forum_system_api.config import get_env_variable


class TestConfig(unittest.TestCase):
    def setUp(self) -> None:
        self.env_var = 'TEST_ENV_VAR'
        self.value = 'test_value'

    @patch('forum_system_api.config.os.getenv')
    def test_getEnvVariable_returnsValue(self, mock_getenv) -> None:
        # Arrange
        mock_getenv.return_value = self.value
        
        # Act
        result = get_env_variable(self.env_var)
        
        # Assert
        mock_getenv.assert_called_once_with(self.env_var)
        self.assertEqual(self.value, result)

    @patch('forum_system_api.config.os.getenv')
    def test_getEnvVariable_raisesValueError_whenNotSet(self, mock_getenv) -> None:
        # Arrange
        mock_getenv.return_value = None
        
        # Act & Assert
        with self.assertRaises(ValueError) as ctx:
            get_env_variable(self.env_var)
        
        mock_getenv.assert_called_once_with(self.env_var)
        self.assertEqual(
            str(ctx.exception), 
            '{} environment variable is not set.'.format(self.env_var)
        )
