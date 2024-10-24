from enum import Enum


class AccessLevel(Enum):
    """
    Enum representing different access levels.

    Attributes:
        READ (str): Represents read-only access.
        WRITE (str): Represents read-write access.

    Methods:
        from_string(value: str) -> 'AccessLevel':
            Converts a string to an AccessLevel enum member.
    """
    READ = 'read_only'
    WRITE = 'read_write'

    @classmethod
    def from_string(cls, value: str) -> 'AccessLevel':
        """
        Create an instance of AccessLevel from a string.

        Args:
            value (str): The string representation of the access level.

        Returns:
            AccessLevel: An instance of the AccessLevel class.
        """
        return cls(value)
