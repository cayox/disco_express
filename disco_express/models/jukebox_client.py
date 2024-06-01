import logging
import os.path
from enum import Enum
from typing import Any

import requests
from pydantic import BaseModel


class JukeBoxConnectionError(Exception):
    """Error indicating the Jukebox Server cannot be reached."""


class ServerStatus(Enum):
    """All available server status."""

    OK = "OK"
    UNAVAILABLE = "UNAVAILABLE"
    SHUTDOWN = "SHUTDOWN"
    ERROR = "ERROR"


class MusicRequest(BaseModel):
    """The Schema of the music request sent to the server."""

    title: str
    interpret: str
    sender: str | None = None
    receiver: str | None = None
    message: str | None = None


class JukeBoxError(BaseModel):
    """The Schema of the errors retrieved from the server."""

    status: int
    error: str


class BannerSchema(BaseModel):
    """The Schema of the banners retrieved from the server."""

    german: str
    english: str


HTTP_OK_RANGE = 200, 299


def status_ok(status: int) -> bool:
    """Function to check for an acceptable http status."""
    return HTTP_OK_RANGE[0] <= status <= HTTP_OK_RANGE[1]


class JukeBoxClient:
    """Class handling the communication with the DiscoExpress Server.

    Args:
        address: the ip/domain address of the server
        port: the port the server is running on
    """

    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port

    def request(
        self,
        method: str,
        uri: str,
        data: dict[str, Any] or None = None,
    ) -> tuple[requests.Response | None, JukeBoxError | None]:
        """Method to make a proper request to the disco_express_server.

        Args:
            method: the request method used
            uri: the uri to which the request should be made
            data: additional adata which should be sent in the body

        Returns:
            The response from the server or None if an error occurred.
        """
        uri = f"http://{self.address}:{self.port}/{uri if not uri.startswith('/') else uri[1:]}"

        headers = {"Content-Type": "application/json"}
        logging.debug("Sending to %s this data: %s", uri, data)
        try:
            response = requests.request(
                method, uri, json=data, headers=headers, timeout=10,
            )
        except requests.exceptions.ConnectionError as exc:
            raise JukeBoxConnectionError(str(exc)) from exc
        if status_ok(response.status_code):
            return response, None

        body = response.json()
        logging.debug("Request unsuccessful: (%s) %s", response.status_code, body)
        error_msg = body.get("error", body.get("detail", str(body)))
        return None, JukeBoxError(status=response.status_code, error=error_msg)

    def send_music_request(self, music_request: MusicRequest) -> None | JukeBoxError:
        """Send a `music_request` to the server."""
        logging.info("Requesting Music: %s", music_request)
        try:
            response, err = self.request(
                "POST",
                "/music_wish/",
                data=music_request.dict(),
            )
            if err is not None:
                return err
        except requests.exceptions.ConnectionError as exc:
            raise JukeBoxConnectionError(str(exc)) from exc

    def get_status(self) -> ServerStatus:
        """Retrieve the current status from the server."""
        response, err = self.request("GET", "/status/")
        if err is not None:
            raise JukeBoxConnectionError(str(err))
        body = response.json()
        return ServerStatus(body["status"])

    def list_documents(self) -> list[str]:
        """Retrieve a list of all available documents from the server."""
        response, err = self.request("GET", "/documents/")
        if err is not None:
            raise JukeBoxConnectionError(str(err))
        return response.json()

    def get_document(self, doc_name: str, save_dir: str) -> str:
        """Retrieve a specific document from the server.

        Args:
            doc_name: the document name which should be retrieved
            save_dir: the directory where the document should be saved.

        Returns:
            the path to the saved document
        """
        response, err = self.request("GET", f"/documents/{doc_name}")
        if err is not None:
            raise JukeBoxConnectionError(str(err))

        # Save the file to local disk
        save_path = os.path.join(save_dir, doc_name)
        with open(save_path, "wb") as file:
            file.write(response.content)
        logging.info("Downloaded '%s' successfully.", doc_name)
        return save_path

    def get_banner_texts(self) -> BannerSchema:
        """Retrieve the banner texts from the server."""
        response, err = self.request("GET", "/banner/")
        if err is not None:
            raise JukeBoxConnectionError(str(err))

        body = response.json()
        return BannerSchema(**body)
