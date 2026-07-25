from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_host: str
    db_port: int = 5432
    db_user: str
    db_password: str
    db_name: str

    class Config:
        env_file = ".env"

settings = Settings()