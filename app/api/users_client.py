import requests
from typing import Dict, Any
from voluptuous import Schema, All, Length, PREVENT_EXTRA


def _validate(data: Dict[str, Any], schema: Schema) -> Dict[str, Any]:
    """Валидация данных по схеме"""
    return schema(data)


class UserApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()

        # Схемы валидации
        self._user_schema = Schema(
            {
                "id": int,
                "email": str,
                "first_name": str,
                "last_name": str,
                "avatar": str
            },
            extra=PREVENT_EXTRA,
            required=True
        )

        self._user_list_schema = Schema(
            {
                "page": int,
                "per_page": int,
                "total": int,
                "total_pages": int,
                "data": All([self._user_schema], Length(min=1)),
                "support": {
                    "url": str,
                    "text": str
                }
            }
        )

    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание пользователя"""
        url = f"{self.base_url}/api/users/"
        response = self.session.post(url, json=user_data)
        response.raise_for_status()
        return _validate(response.json(), self._user_schema)

    def get_users(self) -> Dict[str, Any]:
        """Получение списка пользователей"""
        url = f"{self.base_url}/api/users/"
        response = self.session.get(url)
        response.raise_for_status()
        return _validate(response.json(), self._user_list_schema)

    def get_user(self, user_id: int) -> Dict[str, Any]:
        """Получение пользователя по ID"""
        url = f"{self.base_url}/api/users/{user_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return _validate(response.json(), self._user_schema)

    def update_user(self, user_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Обновление пользователя"""
        url = f"{self.base_url}/api/users/{user_id}"
        response = self.session.patch(url, json=update_data)
        response.raise_for_status()
        return _validate(response.json(), self._user_schema)

    def delete_user(self, user_id: int) -> None:
        """Удаление пользователя"""
        url = f"{self.base_url}/api/users/{user_id}"
        response = self.session.delete(url)
        response.raise_for_status()