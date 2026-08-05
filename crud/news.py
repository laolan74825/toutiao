from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.news import Category, News


# 新闻分类
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


# 新闻列表
async def get_news_list(
    db: AsyncSession, category_id: int, offset: int = 0, limit: int = 10
):
    stmt = (
        select(News).filter(News.category_id == category_id).offset(offset).limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


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
    return [{ "id": news.id,
            "title": news.title,
            "content": news.content,
            "image": news.image,
            "author": news.author,
            "publish_time": news.publish_time,
            "category_id": news.category_id,
            "views": news.views} for news in related_news]
