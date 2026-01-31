from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from pathlib import Path



class Settings(BaseSettings):
    # DB
    db_host: str
    db_port: int
    db_user: str
    db_pass: SecretStr
    db_name: str

    #UVICORN
    host: str
    port: int

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:"
            f"{self.db_pass.get_secret_value()}@"
            f"{self.db_host}:{self.db_port}/"
            f"{self.db_name}"
        )



    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).resolve().parent.parent / ".env"),
        env_file_encoding='utf-8'
    )


settings = Settings()
