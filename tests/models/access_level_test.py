import unittest

from forum_system_api.persistence.models.access_level import AccessLevel


class TestAccessLevel_Should(unittest.TestCase):

    def test_accessLevelRead_returnsCorrectValue(self):
        # Arrange & Act
        result = AccessLevel.READ.value

        # Assert
        self.assertEqual(result, "read_only")

    def test_accessLevelWrite_returnsCorrectValue(self):
        # Arrange & Act
        result = AccessLevel.WRITE.value

        # Assert
        self.assertEqual(result, "read_write")

    def test_fromStringRead_returnsAccessLevelRead(self):
        # Arrange & Act
        result = AccessLevel.from_string("read_only")

        # Assert
        self.assertEqual(result, AccessLevel.READ)

    def test_fromStringWrite_returnsAccessLevelWrite(self):
        # Arrange & Act
        result = AccessLevel.from_string("read_write")

        # Assert
        self.assertEqual(result, AccessLevel.WRITE)

    def test_fromStringInvalid_raisesValueError(self):
        # Act & Assert
        with self.assertRaises(ValueError):
            AccessLevel.from_string("invalid_value")
