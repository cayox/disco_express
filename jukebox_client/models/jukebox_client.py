import requests
from typing import Any
from pydantic import BaseModel

class JukeBoxConnectionError(Exception):
    """Error indicating the Jukebox Server cannot be reached."""


class MusicRequest(BaseModel):
    title: str
    interpret: str
    sender: str | None = None
    receiver: str | None = None
    message: str | None = None


class JukeBoxError(BaseModel):
    status: int
    error: str


def status_ok(status: int) -> bool:
    return 200 <= status <= 299


class JukeBoxClient:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port

    def request(
        self, method: str, uri: str, data: dict[str, Any] or None = None
    ) -> tuple[requests.Response | None, JukeBoxError | None]:
        uri = f"http://{self.address}:{self.port}/{uri if not uri.startswith('/') else uri[1:]}"

        headers = {"Content-Type": "application/json"}
        response = requests.request(method, uri, json=data, headers=headers)
        if status_ok(response.status_code):
            return response, None
        body = response.json()
        error_msg = body.get("error", body.get("detail", str(body)))
        return None, JukeBoxError(**dict(status=response.status_code, error=error_msg))

    def send_music_request(self, music_request: MusicRequest) -> None | JukeBoxError:
        try:
            response, err = self.request("POST", "/music_wish", data=music_request.dict())
            if err is not None:
                return err
        except requests.exceptions.ConnectionError as exc:
            raise JukeBoxConnectionError(str(exc))

    def heartbeat(self) -> bool:
        self.request("GET", "/heartbeat")
