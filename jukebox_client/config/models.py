from pydantic import BaseModel


class Song(BaseModel):
    title: str
    artist: str


class ColorsConfig(BaseModel):
    background_color: str
    text_color: str
    highlight: str
    icon_color: str

    yellow: str
    accent: str
    cream: str
    gray: str
    white: str

    disabled_light: str
    disabled: str
    disabled_dark: str


class LanguageConfig(BaseModel):
    language_name: str
    language_icon: str

    music_title: str
    music_interpret: str
    music_sender: str
    music_receiver: str
    music_message: str

    btn_quick_selection: str
    btn_info: str
    btn_send: str

    error_no_title: str
    error_no_interpret: str
    error_slur_found: str
    error_dj_unavailable: str
    error_network: str
    error_no_connection_to_server: str

    quick_selection_artist_description: str
    quick_selection_song_description: str

    document_names: list[str]


class NetworkConfig(BaseModel):
    server_ip: str
    server_port: int


class GeneralConfig(BaseModel):
    debug: bool
    app_name: str
    quick_selection_file: str
    slurs_file: str
    documents: list[str]

    auto_close_time: int
    server_refresh_interval: int

    artist_icon: str
    song_icon: str
    file_icon: str


class Config(BaseModel):
    general: GeneralConfig
    colors: ColorsConfig
    languages: list[LanguageConfig]
    network: NetworkConfig
