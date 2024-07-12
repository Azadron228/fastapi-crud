from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://shoqan:password@localhost/shoqan"

settings = Config()