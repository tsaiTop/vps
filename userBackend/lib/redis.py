from db.redis_pool import create_redis_connect


async def get_redis_pool():
    """
    获取 Redis 连接池
    """
    return create_redis_connect()
def set_value(key, value):
    """
    设置 Redis 中指定 key 的值
    """
    conn = create_redis_connect()
    conn.set(key, value)
        

async def get_value(key):
    """
    获取 Redis 中指定 key 的值
    """
    redis = create_redis_connect()
    async with redis.client() as conn:
      value =  await conn.get(key)
      return value

async def set_value_with_expire(key, value, expire_seconds):
    """
    设置 Redis 中指定 key 的值，并设置过期时间（秒）
    """
    redis = create_redis_connect()
    async with redis.client() as conn:
      await conn.setex(key, expire_seconds, value)
        
async def delete_key(key):
    """
    删除 Redis 中指定 key
    """
    redis = create_redis_connect()
    async with redis.get() as conn:
        await conn.delete(key)