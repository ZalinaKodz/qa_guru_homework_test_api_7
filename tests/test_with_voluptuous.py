import pytest
import json
import os
from datetime import datetime

import requests

from app.api.users_client import UserApiClient


@pytest.fixture(scope="module")
def api_client(app_url):
    """Фикстура для API клиента"""
    return UserApiClient(base_url=app_url)


@pytest.fixture(scope="module")
def test_users_data():
    """Загрузка тестовых данных"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    users_json_path = os.path.join(current_dir, "..", "users.json")
    with open(users_json_path, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="module")
def created_users(api_client, test_users_data):
    """Фикстура с созданными пользователями"""
    users = []
    for user_data in test_users_data:
        users.append(api_client.create_user(user_data))
    yield users
    for user in users:
        api_client.delete_user(user["id"])


def test_create_user(api_client):
    """Тест создания пользователя"""
    user_data = {
        "email": f"test_{datetime.now().timestamp()}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "avatar": "http://example.com/avatar.png"
    }

    # Создание и валидация
    user = api_client.create_user(user_data)
    assert user["email"] == user_data["email"]

    # Проверка через GET
    fetched_user = api_client.get_user(user["id"])
    assert fetched_user["email"] == user_data["email"]


def test_user_lifecycle(api_client):
    """Полный цикл тестирования"""
    user_data = {
        "email": f"lifecycle_{datetime.now().timestamp()}@example.com",
        "first_name": "Lifecycle",
        "last_name": "Test",
        "avatar": "http://example.com/avatar.png"  # Явно передаем avatar
    }

    user = api_client.create_user(user_data)
    assert user["email"] == user_data["email"]

    # Чтение
    fetched_user = api_client.get_user(user["id"])
    assert fetched_user["first_name"] == "Lifecycle"

    # Обновление
    updated_user = api_client.update_user(user["id"], {"first_name": "Updated"})
    assert updated_user["first_name"] == "Updated"

    # Удаление
    api_client.delete_user(user["id"])

    # Проверка удаления
    with pytest.raises(requests.exceptions.HTTPError):
        api_client.get_user(user["id"])


def test_invalid_email(api_client):
    """Тест невалидного email"""
    with pytest.raises(requests.exceptions.HTTPError):
        api_client.create_user({
            "email": "invalid-email",
            "first_name": "Invalid",
            "last_name": "Email"
        })


def test_nonexistent_user(api_client):
    """Тест работы с несуществующим пользователем"""
    with pytest.raises(requests.exceptions.HTTPError):
        api_client.get_user(99999)