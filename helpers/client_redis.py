from redis.asyncio import Redis

from settings import RedisConfig


redis = Redis(
    host=RedisConfig.REDIS_HOST,
    port=RedisConfig.REDIS_PORT,
    db=RedisConfig.REDIS_DB,
    password=RedisConfig.REDIS_PASSWORD,
    decode_responses=True,
)


async def get_redis():
    return redis
