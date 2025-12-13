from pydantic_settings import BaseSettings
from typing import Literal
from urllib.parse import quote_plus


class Settings(BaseSettings):
    DB_TYPE: Literal["mysql", "postgres", "sqlite"]

    # Common
    DB_USER: str | None = None
    DB_PASSWORD: str | None = None
    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_NAME: str | None = None

    # SQLite only
    SQLITE_PATH: str | None = None

    @property
    def DATABASE_URL(self) -> str:
        if self.DB_TYPE == "mysql":
            self._validate_mysql()
            password = quote_plus(self.DB_PASSWORD)
            return (
                f"mysql+mysqlconnector://{self.DB_USER}:"
                f"{password}@{self.DB_HOST}:{self.DB_PORT}/"
                f"{self.DB_NAME}?charset=utf8mb4"
            )

        if self.DB_TYPE == "postgres":
            self._validate_postgres()
            password = quote_plus(self.DB_PASSWORD)
            return (
                f"postgresql+psycopg2://{self.DB_USER}:"
                f"{password}@{self.DB_HOST}:{self.DB_PORT}/"
                f"{self.DB_NAME}"
            )

        if self.DB_TYPE == "sqlite":
            self._validate_sqlite()
            return f"sqlite:///{self.SQLITE_PATH}"

        raise ValueError(f"Unsupported DB_TYPE: {self.DB_TYPE}")

    # ===== VALIDATORS =====

    def _validate_mysql(self):
        required = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
        self._check_required(required)

    def _validate_postgres(self):
        required = ["DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT", "DB_NAME"]
        self._check_required(required)

    def _validate_sqlite(self):
        if not self.SQLITE_PATH:
            raise ValueError("SQLITE_PATH is required when DB_TYPE=sqlite")

    def _check_required(self, fields: list[str]):
        for field in fields:
            if getattr(self, field) in (None, ""):
                raise ValueError(f"{field} is required when DB_TYPE={self.DB_TYPE}")

    class Config:
        env_file = ".env"


settings = Settings()
