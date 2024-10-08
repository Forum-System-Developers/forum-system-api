from enum import Enum


class AccessLevel(Enum):
    READ = 'read_only'
    WRITE = 'read_write'

    @classmethod
    def from_string(cls, value: str) -> 'AccessLevel':
        return cls(value)
