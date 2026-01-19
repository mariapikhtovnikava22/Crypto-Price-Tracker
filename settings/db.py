from settings.base import env


class DbConfig:
    CONNECTION_SETTINGS = {
        "dsn": env.str("DB_URL", default="postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"),
    }
