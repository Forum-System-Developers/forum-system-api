import os

from dotenv import load_dotenv

load_dotenv()


def get_env_variable(name: str) -> str:
    """
    Get the value of the specified environment variable.

    Args:
        name (str): The name of the environment variable.

    Returns:
        str: The value of the environment variable.

    Raises:
        ValueError: If the environment variable is not set.
    """
    value = os.getenv(name)
    if value is None:
        raise ValueError(f"{name} environment variable is not set.")
    return value


DATABASE_URL = get_env_variable("DATABASE_URL")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

SECRET_KEY = get_env_variable("SECRET_KEY")
ALGORITHM = get_env_variable("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env_variable("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(get_env_variable("REFRESH_TOKEN_EXPIRE_DAYS"))
