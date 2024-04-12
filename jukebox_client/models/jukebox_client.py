import requests
from pydantic import BaseModel


class MusicRequest(BaseModel):
    title: str
    interpret: str
    sender: str | None = None
    receiver: str | None = None
    message: str | None = None


class JukeBoxError(BaseModel):
    status: str
    error: str


def status_ok(status: int) -> bool:
    return 200 <= status <= 299


class JukeBoxClient:
    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port

    def request(
        self, method: str, uri: str, data: dict or None = None
    ) -> tuple[requests.Response | None, JukeBoxError | None]:
        uri = f"http://{self.address}:{self.port}/{uri}"

        response = requests.request(method, uri, data=data)
        if status_ok(response.status_code):
            return response, None
        return None, JukeBoxError(**response.json())

    def send_music_request(self, music_request: MusicRequest) -> None | JukeBoxError:
        response, err = self.request("POST", "/music-wish", data=music_request.__dict__)
        if err is not None:
            return err
