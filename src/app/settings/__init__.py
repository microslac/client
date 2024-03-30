from .base import EnvSettings
from .jwt import JwtSettings
from .general import ApiSettings, CorsSettings
from .database import DatabaseSettings

__all__ = ["settings"]


class Settings(EnvSettings):
    api: ApiSettings = ApiSettings()
    cors: CorsSettings = CorsSettings()
    db: DatabaseSettings = DatabaseSettings()
    jwt: JwtSettings = JwtSettings()


settings = Settings()
