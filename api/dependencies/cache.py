# Cache DB dependency
from aiocache import Cache
from aiocache.serializers import JsonSerializer

from api.internal.config import get_settings

__CONNECTION_STRING = get_settings().API_CACHEDB_URL

cache = Cache.from_url(__CONNECTION_STRING, serializer=JsonSerializer())

async def get_cache():
    return cache

"""
# example usage:
# from https://loadforge.com/guides/database-performance-tuning-for-high-speed-fastapi-web-services
async def read_item(item_id: int, cache: Cache = Depends(get_cache)):
    cache_key = f"item_{item_id}"
    item = await cache.get(cache_key)
    if item is not None:
        return item
    item = await get_item_from_db(item_id)
    await cache.set(cache_key, item, ttl=300)
    return item
"""