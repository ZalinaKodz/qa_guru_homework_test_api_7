import pytest
import os
from dotenv import load_dotenv

load_dotenv()

def pytest_addoption(parser):
    parser.addoption(
        "--env",
        default="dev",
        help="Environment to run tests against: local or prod"
    )

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def app_url(env):
    if env == "dev":
        return os.getenv("APP_URL", "http://127.0.0.1:8002")
    elif env == "prod":
        return os.getenv("APP_URL_PROD", "https://your-production-url.com")
    else:
        raise ValueError(f"Unknown environment: {env}")

@pytest.fixture(scope="session")
def api_client(app_url):
    from app.api.users_client import UserApiClient
    return UserApiClient(base_url=app_url)