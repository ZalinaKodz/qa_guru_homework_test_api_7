import pytest
import json
import os
from datetime import datetime
from requests.exceptions import HTTPError

from app.api.users_client import UserApiClient
from config import Server


@pytest.fixture(scope="session")
def api_client(env):
    """Фикстура для API клиента с настройкой окружения"""
    base_url = Server(env).reqres
    return UserApiClient(base_url=base_url)


@pytest.fixture(scope="module")
def test_users_data():
    """Загрузка тестовых данных из JSON файла"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    users_json_path = os.path.join(current_dir, "..", "users.json")
    with open(users_json_path, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def created_users(api_client, test_users_data):
    """Фикстура с созданными пользователями (удаляются после тестов)"""
    users = []
    for user_data in test_users_data:
        try:
            user = api_client.create_user(user_data)
            users.append(user)
        except HTTPError as e:
            pytest.fail(f"Failed to create test user: {str(e)}")

    yield users

    for user in users:
        try:
            api_client.delete_user(user["id"])
        except HTTPError:
            pass  # Пользователь уже удален


def test_create_and_get_user(api_client):
    """Тест создания и получения пользователя"""
    user_data = {
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "avatar": "http://example.com/avatar.png"
    }

    # Тест создания
    user = api_client.create_user(user_data)
    assert all(k in user for k in ["id", "email", "first_name", "last_name"])

    # Тест получения
    fetched_user = api_client.get_user(user["id"])
    assert fetched_user["email"] == user_data["email"]
    assert fetched_user["first_name"] == user_data["first_name"]


def test_user_lifecycle(api_client):
    """Полный цикл CRUD операций с пользователем"""
    # Create
    user_data = {
        "email": f"lifecycle_{datetime.now().timestamp()}@example.com",
        "first_name": "Lifecycle",
        "last_name": "Test",
        "avatar": "http://example.com/avatar.png"
    }
    user = api_client.create_user(user_data)

    # Read
    fetched_user = api_client.get_user(user["id"])
    assert fetched_user["first_name"] == "Lifecycle"

    # Update
    updated_data = {"first_name": "UpdatedName", "last_name": "UpdatedLastName"}
    updated_user = api_client.update_user(user["id"], updated_data)
    assert updated_user["first_name"] == "UpdatedName"
    assert updated_user["last_name"] == "UpdatedLastName"

    # Delete
    api_client.delete_user(user["id"])
    with pytest.raises(HTTPError) as exc_info:
        api_client.get_user(user["id"])
    assert exc_info.value.response.status_code == 404


def test_invalid_data_handling(api_client):
    """Тест обработки невалидных данных"""
    # Невалидный email
    with pytest.raises(HTTPError) as exc_info:
        api_client.create_user({
            "email": "invalid-email",
            "first_name": "Invalid",
            "last_name": "Email"
        })
    assert exc_info.value.response.status_code in [400, 422]

    # Неполные данные
    with pytest.raises(HTTPError):
        api_client.create_user({
            "email": "test@example.com",
            # Нет обязательных first_name и last_name
        })


def test_nonexistent_user_operations(api_client):
    """Тест операций с несуществующим пользователем"""
    non_existent_id = 99999

    # Получение
    with pytest.raises(HTTPError) as exc_info:
        api_client.get_user(non_existent_id)
    assert exc_info.value.response.status_code == 404

    # Обновление
    with pytest.raises(HTTPError) as exc_info:
        api_client.update_user(non_existent_id, {"first_name": "Test"})
    assert exc_info.value.response.status_code == 404

    # Удаление
    with pytest.raises(HTTPError) as exc_info:
        api_client.delete_user(non_existent_id)
    assert exc_info.value.response.status_code == 404