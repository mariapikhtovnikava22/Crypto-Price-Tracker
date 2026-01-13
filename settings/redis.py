from .base import env


class RedisConfig:
    REDIS_HOST = env.str("REDIS_HOST", default="localhost")
    REDIS_PORT = env.int("REDIS_PORT", default=6379)
    REDIS_DB = env.int("REDIS_DB", default=0)
    REDIS_PASSWORD = env.str("REDIS_PASSWORD", default=None)

    @classmethod
    def get_settings(cls) -> dict:
        return {
            "host": cls.REDIS_HOST,
            "port": cls.REDIS_PORT,
            "db": cls.REDIS_DB,
            "password": cls.REDIS_PASSWORD,
            "decode_responses": True,
        }
