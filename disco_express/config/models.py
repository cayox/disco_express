# ruff: noqa: D101
from pydantic import BaseModel


class Song(BaseModel):
    title: str
    artist: str
    plays: int = 0


class ColorsConfig(BaseModel):
    background_color: str

    accent1: str
    accent1_glow: str
    accent1_dark: str

    highlight_glow: str
    highlight: str
    off_highlight: str

    icon_color: str

    white: str
    red: str

    disabled_light: str
    disabled: str
    disabled_dark: str


class StyleConfig(BaseModel):
    background_image: str
    background_darkness_factor: float = 0.5
    colors: ColorsConfig
    ui_glow_strength: int
    text_glow_strength: int


class LanguageConfig(BaseModel):
    language_name: str
    language_icon: str

    heading_music_wish: str
    heading_home: str
    heading_information: str

    home_info_btn: str
    home_music_wish_btn: str

    music_title: str
    music_interpret: str
    music_sender: str
    music_receiver: str
    music_message: str

    btn_quick_selection: str
    btn_send: str

    error_no_title: str
    error_no_interpret: str
    error_slur_found: str
    error_dj_unavailable: str
    error_network: str
    error_no_connection_to_server: str

    classics_artist_description: str
    classics_song_description: str

    loading_description: list[str]
    loading_success: str

    rotating_banner: str = "---"


class NetworkConfig(BaseModel):
    server_ip: str
    server_port: int


class IconsConfig(BaseModel):
    artist_icon: str
    song_icon: str
    file_icon: str
    error_icon: str
    home_icon: str
    charts_plays_icon: str
    unavailable_icon: str
    zoom_in_icon: str
    zoom_out_icon: str


class GeneralConfig(BaseModel):
    debug: bool
    app_name: str

    classics_file: str
    charts_file: str
    slurs_file: str
    current_charts: str

    documents_directory: str
    log_directory: str

    auto_close_time: int
    server_refresh_interval: int
    wish_sending_time: int
    banner_speed: int

    max_input_length: int
    max_input_length_message: int


class Config(BaseModel):
    general: GeneralConfig
    icons: IconsConfig
    style: StyleConfig
    languages: list[LanguageConfig]
    network: NetworkConfig
    selected_language: LanguageConfig | None = None
