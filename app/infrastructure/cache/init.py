from redis.asyncio import Redis

from infrastructure.cache.config import CacheConfig


def init_cache(cache_config: CacheConfig) -> Redis:
    return Redis(host=cache_config.host, port=cache_config.port)
