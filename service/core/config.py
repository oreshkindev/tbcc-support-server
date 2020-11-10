import databases

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

config = Config(".env")


PREFIX = "/api/v1"

VERSION = "0.0.1"

DEBUG: bool = config("DEBUG", cast=bool, default=False)

DB_USER: str = config("DB_USER")
DB_PASSWORD: str = config("DB_PASSWORD")
DB_NAME: str = config("DB_NAME")
DB_HOST: str = config("DB_HOST", default="localhost")

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

PROJECT_NAME: str = config("PROJECT_NAME", default="Example service")

CLIENT_SESSION: str = config("CLIENT_SESSION")
CLIENT_API_ID: str = config("CLIENT_API_ID")
CLIENT_API_HASH: str = config("CLIENT_API_HASH")