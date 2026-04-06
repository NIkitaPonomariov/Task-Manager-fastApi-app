from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    DATABASE_URL: str 
    cors_allowd_origin: list[str]


def get_settings() -> Settings:
    return Settings(
        DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/taskmanager",
        cors_allowd_origin = ["http://localhost:3000"],
    )