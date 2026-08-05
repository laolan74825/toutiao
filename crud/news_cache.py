from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from cache.news_cache import (
    get_cached_categories,
    get_cached_news_list,
    set_cache_categories,
    set_cache_news_list,
)
from models.news import Category, News
from schemas.base import NewsItemBase


# 新闻分类
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    cached_categories = await get_cached_categories()
    if cached_categories:
        print("从缓存中获取新闻分类")
        return cached_categories

    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    categories = result.scalars().all()

    if categories:
        categories = jsonable_encoder(categories)
        await set_cache_categories(categories)
    return categories


# 新闻列表
async def get_news_list(
    db: AsyncSession, category_id: int, offset: int = 0, limit: int = 10
):
    page = offset // limit + 1
    cached_news_list = await get_cached_news_list(category_id, page, limit)
    if cached_news_list:
        print("从缓存中获取新闻列表")
        return [News(**item) for item in cached_news_list]

    stmt = (
        select(News).filter(News.category_id == category_id).offset(offset).limit(limit)
    )
    result = await db.execute(stmt)
    news_list = result.scalars().all()

    if news_list:
        # news_list = jsonable_encoder(news_list)   原转换方法
        news_list = [
            NewsItemBase.model_validate(item).model_dump(mode="json", by_alias=False)
            for item in news_list
        ]
        await set_cache_news_list(category_id, page, limit, news_list)

    return news_list


# 新闻总数
async def get_news_total(db: AsyncSession, category_id: int):
    stmt = select(func.count(News.id)).filter(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()


# 新闻详情
async def get_news_detail(db: AsyncSession, news_id: int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


# 新闻浏览量
async def update_news_views(db: AsyncSession, news_id: int):
    update_stmt = update(News).where(News.id == news_id).values(views=News.views + 1)

    result = await db.execute(update_stmt)
    await db.commit()

    return result.rowcount > 0  # pyright: ignore[reportAttributeAccessIssue]


# 相关新闻
async def get_related_news(
    db: AsyncSession, news_id: int, category_id: int, limit: int = 5
):
    stmt = (
        select(News)
        .where(News.category_id == category_id, News.id != news_id)
        .order_by(News.views.desc(), News.publish_time.desc())
        .limit(limit)
    )
    result = await db.execute(stmt)
    # return result.scalars().all()

    related_news = result.scalars().all()
    return [
        {
            "id": news.id,
            "title": news.title,
            "content": news.content,
            "image": news.image,
            "author": news.author,
            "publish_time": news.publish_time,
            "category_id": news.category_id,
            "views": news.views,
        }
        for news in related_news
    ]
