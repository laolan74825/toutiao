import json
from typing import Any

import redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# 创建 Redis 连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,  # decode_responses=True是告诉Redis返回字符串，而不是字节
)


# 设置 和 读取 （字符串 和 列表或字典）
# 读取：字符串
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None


# 读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data)
    except Exception as e:
        print(f"获取JSON缓存失败: {e}")
        return None


# 设置缓存
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)):
            value = json.dumps(
                value, ensure_ascii=False
            )  # ensure_ascii=False 中文正常保存
        await redis_client.setex(key, expire, value)
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False
