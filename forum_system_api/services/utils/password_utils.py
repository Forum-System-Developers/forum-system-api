import logging

from passlib.context import CryptContext


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    """
    Hashes the given password using bcrypt.
    """
    hash_password = context.hash(password)
    logger.info("Password hashed")

    return hash_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that the given plain password matches the hashed password.
    """
    password = context.verify(plain_password, hashed_password)
    logger.info("Password verified")

    return password
