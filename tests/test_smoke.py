import os
import pytest
import requests
import json
from datetime import datetime

@pytest.fixture(scope="module")
def fill_test_data(app_url):
    """Fixture для заполнения тестовых данных перед тестами."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    users_json_path = os.path.join(current_dir, "..", "users.json")
    with open(users_json_path, encoding="utf-8") as f:
        test_data_users = json.load(f)

    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        assert response.status_code == 201, f"Failed to create user: {user}"
        api_users.append(response.json())

    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")

def test_create_user(app_url):
    """Тест на создание пользователя (POST)."""
    payload = {
        "email": f"user_{datetime.now().microsecond}@example.com",
        "first_name": "Test",
        "last_name": "User",
        "avatar": "http://example.com/test-avatar.png"
    }
    response = requests.post(f"{app_url}/api/users/", json=payload)
    assert response.status_code == 201, f"Create user failed with status code {response.status_code}"
    data = response.json()
    assert "id" in data, "Response does not contain user ID"
    assert data["email"] == payload["email"], "User email does not match"

def test_delete_user(app_url, fill_test_data):
    """Тест на удаление пользователя (DELETE)."""
    user_id = fill_test_data[0]
    response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert response.status_code == 204, f"Delete user failed with status code {response.status_code}"

    # Проверка, что пользователь удален
    response_get = requests.get(f"{app_url}/api/users/{user_id}")
    assert response_get.status_code == 404, f"User {user_id} was not deleted"

def test_patch_user(app_url, fill_test_data):
    """Тест на изменение пользователя (PATCH)."""
    user_id = fill_test_data[1]
    update_payload = {"first_name": "UpdatedName"}
    response = requests.patch(f"{app_url}/api/users/{user_id}", json=update_payload)
    assert response.status_code == 200, f"Patch user failed with status code {response.status_code}"
    assert response.json()["first_name"] == "UpdatedName", "User first name was not updated"

    # Проверка измененного имени
    response_get = requests.get(f"{app_url}/api/users/{user_id}")
    assert response_get.status_code == 200, f"Get user failed after patch with status code {response_get.status_code}"
    assert response_get.json()["first_name"] == "UpdatedName", "User first name was not updated"


def test_get_user_after_update(app_url, fill_test_data):
    """Тест на получение пользователя (GET) после обновления."""
    user_id = fill_test_data[1]
    update_payload = {"last_name": "UpdatedLastname"}
    response_patch = requests.patch(f"{app_url}/api/users/{user_id}", json=update_payload)
    assert response_patch.status_code == 200, f"Patch user failed with status code {response_patch.status_code}"

    response_get = requests.get(f"{app_url}/api/users/{user_id}")
    assert response_get.status_code == 200, f"Get user failed after patch with status code {response_get.status_code}"
    assert response_get.json()["last_name"] == "UpdatedLastname", "User last name was not updated"

def test_user_flow(app_url):
    """Тест на создание -> чтение -> обновление -> удаление."""
    payload = {
        "email": f"user_{datetime.now().microsecond}@example.com",
        "first_name": "Flow",
        "last_name": "User",
        "avatar": "http://example.com/flow-avatar.png"
    }

    # Создание пользователя
    create_response = requests.post(f"{app_url}/api/users/", json=payload)
    assert create_response.status_code == 201, "Failed to create user"
    user_id = create_response.json()["id"]

    # Чтение пользователя
    get_response = requests.get(f"{app_url}/api/users/{user_id}")
    assert get_response.status_code == 200, "Failed to get user"
    assert get_response.json()["email"] == payload["email"], "User email does not match"

    # Обновление пользователя
    update_payload = {"first_name": "UpdatedFlow"}
    update_response = requests.patch(f"{app_url}/api/users/{user_id}", json=update_payload)
    assert update_response.status_code == 200, "Failed to update user"
    assert update_response.json()["first_name"] == "UpdatedFlow", "User first name was not updated"

    # Удаление пользователя
    delete_response = requests.delete(f"{app_url}/api/users/{user_id}")
    assert delete_response.status_code == 204, "Failed to delete user"

    # Проверка удаления
    final_check = requests.get(f"{app_url}/api/users/{user_id}")
    assert final_check.status_code == 404, "User was not deleted"

def test_create_user_invalid_email(app_url):
    """Тест на создание пользователя с недопустимым email."""
    payload = {
        "email": "invalid-email",
        "first_name": "Invalid",
        "last_name": "Email",
        "avatar": "http://example.com/avatar.png"
    }
    response = requests.post(f"{app_url}/api/users/", json=payload)
    assert response.status_code == 422, "Validation error not returned for invalid email"

def test_patch_nonexistent_user(app_url):
    """Тест на обновление несуществующего пользователя."""
    response = requests.patch(f"{app_url}/api/users/99999", json={"first_name": "Ghost"})
    assert response.status_code == 404, "404 not returned for nonexistent user"

def test_delete_nonexistent_user(app_url):
    """Тест на удаление несуществующего пользователя."""
    response = requests.delete(f"{app_url}/api/users/99999")
    assert response.status_code == 404, "404 not returned for nonexistent user"

def test_method_not_allowed(app_url):
    """Тест на разрешение методов."""
    response = requests.put(f"{app_url}/api/users/")
    assert response.status_code == 405, "405 not returned for disallowed method"