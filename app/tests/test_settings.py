from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Loading .env.test
load_dotenv(".env.test")


class SettingsTest(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int


test_settings = SettingsTest()

DATABASE_URL = test_settings.DATABASE_URL
SECRET_KEY = test_settings.SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = test_settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS = test_settings.REFRESH_TOKEN_EXPIRE_DAYS
