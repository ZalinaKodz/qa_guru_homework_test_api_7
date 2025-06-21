from typing import Optional, TypeVar, Any
import requests
from requests import Session
from fastapi import HTTPException
from voluptuous import Schema

T = TypeVar('T')


class ApiClient:
    def __init__(self, environment: str = "development"):
        self.environment = environment
        self.session = self._init_session()

    def _init_session(self) -> Session:
        session = requests.Session()
        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        base_urls = {
            "development": "http://localhost:8002",
            "staging": "https://staging.api.example.com",
            "production": "https://api.example.com"
        }
        session.base_url = base_urls[self.environment]
        return session

    def _validate_input(self, data: dict, schema: Schema) -> dict:
        try:
            return schema(data)
        except Exception as e:
            raise ValueError(f"Input validation failed: {str(e)}")

    def _request(
            self,
            method: str,
            endpoint: str,
            *,
            expected_status: int = 200,
            request_schema: Optional[Schema] = None,
            **kwargs
    ) -> Any:
        url = f"{self.session.base_url}{endpoint}"
        if request_schema and 'json' in kwargs:
            kwargs['json'] = self._validate_input(kwargs['json'], request_schema)

        response = self.session.request(method, url, **kwargs)

        if response.status_code != expected_status:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Expected status {expected_status}, got {response.status_code}"
            )

        return response.json() if response.content else None