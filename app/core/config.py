import tomllib
from functools import lru_cache
from pathlib import Path
from pydantic import BaseModel
from typing import Any, Dict


class AppConfig(BaseModel):
    name: str
    env: str
    host: str
    port: int


class DatabaseConfig(BaseModel):
    user: str
    password: str
    host: str
    port: int
    database: str
    echo: bool = False
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 1800


    @property
    def mysql_url(self) -> str:
        # Use UTF-8MB4 for emoji / full Unicode
        return (
            f"mysql+asyncmy://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
            f"?charset=utf8mb4"
        )

class RedisConfig(BaseModel):
    host: str
    port: int
    db: int

class LoggerConfig(BaseModel):
    dir: str
    file: str
    level: str
    rotation: str
    retention: int

class SecretConfig(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expires: int

class Settings(BaseModel):
    app: AppConfig
    database: DatabaseConfig
    redis: RedisConfig
    logger: LoggerConfig
    secret: SecretConfig


def load_config() -> Dict[str, Any]:
    base_path = Path(__file__).resolve().parent.parent.parent

    # 1. 读取主配置
    with open(base_path / "config/config.toml", "rb") as f:
        base_config = tomllib.load(f)

    return base_config


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    toml_config = load_config()

    return Settings(**toml_config)