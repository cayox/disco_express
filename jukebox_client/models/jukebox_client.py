import os.path

import requests
from typing import Any
from pydantic import BaseModel
import logging
from enum import Enum
from jukebox_client.config import CONFIG



class JukeBoxConnectionError(Exception):
    """Error indicating the Jukebox Server cannot be reached."""

class ServerStatus(Enum):
    OK = "OK"
    UNAVAILABLE = "UNAVAILABLE"
    SHUTDOWN = "SHUTDOWN"
    ERROR = "ERROR"

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
        logging.debug(f"Sending to {uri} this data: {data}")
        try:
            response = requests.request(method, uri, json=data, headers=headers)
        except requests.exceptions.ConnectionError as exc:
            raise JukeBoxConnectionError(str(exc))
        if status_ok(response.status_code):
            return response, None

        body = response.json()
        logging.debug(f"Request unsucessful: ({response.status_code}) {body}")
        error_msg = body.get("error", body.get("detail", str(body)))
        return None, JukeBoxError(**dict(status=response.status_code, error=error_msg))

    def send_music_request(self, music_request: MusicRequest) -> None | JukeBoxError:
        logging.info(f"Requesting Music: {music_request}", music_request)
        try:
            response, err = self.request(
                "POST", "/music_wish", data=music_request.dict()
            )
            if err is not None:
                return err
        except requests.exceptions.ConnectionError as exc:
            raise JukeBoxConnectionError(str(exc))

    def get_status(self) -> ServerStatus:
        response, err = self.request("GET", "/status")
        if err is not None:
            raise JukeBoxConnectionError(str(err))
        body = response.json()
        return ServerStatus(body["status"])

    def list_documents(self) -> list[str]:
        response, err = self.request("GET", "/documents")
        if err is not None:
            raise JukeBoxConnectionError(str(err))
        return response.json()

    def get_document(self, doc_name: str) -> str:
        response, err = self.request("GET", f"/documents/{doc_name}")
        if err is not None:
            raise JukeBoxConnectionError(str(err))

        # Save the file to local disk
        save_path = os.path.join(CONFIG.general.documents_directory, doc_name)
        with open(save_path, "wb") as file:
            file.write(response.content)
        logging.info(f"Downloaded '{doc_name}' successfully.")
        return save_path
