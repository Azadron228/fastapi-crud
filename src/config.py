from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://shoqan:password@localhost/shoqan"
    TOKEN_SECRET: str = "0298472a00c80cf31fc7fdc5166fdd6968fd4c7319758362f0e71c361070c346"
    TOKEN_ALGORITHM: str = "HS256"

settings = Config()