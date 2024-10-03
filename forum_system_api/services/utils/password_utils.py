from passlib.context import CryptContext


context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Hashes the given password using bcrypt.
    """
    return context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies that the given plain password matches the hashed password.
    """
    return context.verify(plain_password, hashed_password)
