from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str = 'train_booking'
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'postgres'
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432

    class Config:
        env_file = '.env'