import redis.asyncio as redis

redis_client = None

def init_redis() -> "redis.Redis":
    global redis_client
    connection: "redis.Redis" = redis.Redis(host="redis")
    redis_client = connection
    return connection