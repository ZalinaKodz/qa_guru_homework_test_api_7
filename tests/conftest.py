import os

import pytest
from dotenv import load_dotenv

@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()

@pytest.fixture(scope="module")
def app_url():
    url = os.getenv("APP_URL")
    if url is None:
        raise ValueError("Переменная APP_URL не задана в .env файле")
    return url