import requests
from typing import Any

class queueDB:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"token": token})

    def set_keys(self, data: dict) -> None:
        r = self.session.post(f"{self.base_url}/v1/keys", json=data)
        if r.status_code != 204:
            try:
                err = r.json()
            except Exception:
                err = {"message": r.text, "code": r.status_code}
            raise RuntimeError(f"{err.get('code')}: {err.get('message')}")

    def get_keys(self, keys: list[str]) -> dict:
        r = self.session.get(f"{self.base_url}/v1/keys", json=keys)
        if r.status_code != 200:
            try:
                err = r.json()
            except Exception:
                err = {"message": r.text, "code": r.status_code}
            raise RuntimeError(f"{err.get('code')}: {err.get('message')}")
        return r.json()

    def set_key(self, key: str, value: Any) -> None:
        self.set_keys({key: value})

    def get_key(self, key: str) -> Any:
        res = self.get_keys([key])
        return res.get(key)
