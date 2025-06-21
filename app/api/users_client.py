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

    def create_user(self, user_data: dict):
        response = self.session.post(f"{self.base_url}/api/users/", json=user_data)
        response.raise_for_status()
        return response.json()

    def get_user(self, user_id: int):
        response = self.session.get(f"{self.base_url}/api/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def update_user(self, user_id: int, user_data: dict):
        response = self.session.patch(f"{self.base_url}/api/users/{user_id}", json=user_data)
        response.raise_for_status()
        return response.json()

    def delete_user(self, user_id: int):
        response = self.session.delete(f"{self.base_url}/api/users/{user_id}")
        response.raise_for_status()
        return response.status_code