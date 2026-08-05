# 新闻相关的缓存方法：新闻分类的读取和写入
# key - value
from typing import Any, Dict, List

from config.cache_conf import get_json_cache, set_cache


CATEGORIDS_KEY = "news:categories"
NEWS_LIST_PREFIX = "news:list:"


# 获取新闻分类缓存
async def get_cached_categories():
    return await get_json_cache(CATEGORIDS_KEY)



# 写入新闻分类缓存: 缓存数据，并设置过期时间
# 常用的缓存时间：分类、配置7200秒；列表：600秒；详情：1800秒， 验证码：120秒 --数据越稳定，缓存时间越持久
async def set_cache_categories(data: List[Dict[str, Any]], expire: int = 7200):
    return await set_cache(CATEGORIDS_KEY, data, expire)


# 写入新闻列表缓存
async def set_cache_news_list(
    category_id: int | None ,
    page: int,
    page_size:int,
    data: List[Dict[str, Any]],
    expire: int = 1800,
):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}:{category_part}:{page}:{page_size}"
    return await set_cache(key, data, expire)

# 获取新闻列表缓存
async def get_cached_news_list(
    category_id: int | None,
    page: int,
    page_size:int,
):
    category_part = category_id if category_id is not None else "all"
    key = f"{NEWS_LIST_PREFIX}:{category_part}:{page}:{page_size}"
    return await get_json_cache(key)
