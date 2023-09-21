from environs import Env

env = Env()
env.read_env()


class FastAPISettings:
    API_V1_STR: str = "/api/v1"

    AUTH_JWT_SECRET_KEY: str = env("AUTH_JWT_SECRET_KEY", default="secret")
    AUTH_JWT_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_TIME: int = 5
    REFRESH_TOKEN_EXPIRE_TIME: int = 10

    DB_URI: str = env.str("DB_URI", default="postgresql+asyncpg://user:pass@127.0.0.1:5432/basename")
    ECHO_SQL: bool = env.bool("ECHO_SQL", default=True)


settings = FastAPISettings()
