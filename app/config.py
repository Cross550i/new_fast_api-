from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # DB
    db_url: str

    #UVICORN
    host: str
    port: int

    model_config = SettingsConfigDict(env_file=".env")



settings = Settings()


