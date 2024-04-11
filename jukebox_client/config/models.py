from pydantic import BaseModel


class Colors(BaseModel):
    background_color: str
    text_color: str
    red: str
    yellow: str
    turqoise: str
    cream: str
    gray: str
    white: str


class Language(BaseModel):
    error_no_title: str
    error_no_interpret: str
    error_slur_found: str
    error_dj_unavailable: str
    error_network: str

class Languages(BaseModel):
    english: Language
    german: Language


class General(BaseModel):
    documents: list[str]


class Network(BaseModel):
    server_ip: str
    server_port: str


class Config(BaseModel):
    general: General
    colors: Colors
    languages: Languages
    network: Network
