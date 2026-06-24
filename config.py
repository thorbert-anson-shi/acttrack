from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    tz_zoneinfo: str = Field("Etc/UTC")


settings = Settings()
