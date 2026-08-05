from fastapi import HTTPException
from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.favorite import Favorite
from models.news import News


# 检查新闻是否已收藏
async def check_news_favorite(db: AsyncSession, user_id: int, news_id: int):
    query = select(Favorite).where(
        Favorite.news_id == news_id, Favorite.user_id == user_id
    )
    result = await db.execute(query)
    return result.scalar_one_or_none() is not None


# 添加收藏
async def add_favorite(db: AsyncSession, user_id: int, news_id: int):
    favorite = Favorite(news_id=news_id, user_id=user_id)
    db.add(favorite)

    try:
        await db.commit()
        await db.refresh(favorite)
        return favorite
    except IntegrityError:
        # 捕获数据库的唯一约束冲突异常
        await db.rollback()  # 必须回滚，否则当前 Session 处于失效状态
        raise HTTPException(status_code=400, detail="新闻已收藏")


# 取消收藏
async def remove_favorite(db: AsyncSession, user_id: int, news_id: int):
    query = delete(Favorite).where(
        Favorite.news_id == news_id, Favorite.user_id == user_id
    )
    result = await db.execute(query)
    await db.commit()
    return result.rowcount > 0  # type: ignore


# 获取收藏列表
async def get_favorite_list(
    db: AsyncSession,
    user_id: int,
    page: int = 1,
    page_size: int = 10,
):
    """
    获取收藏列表
    """
    count_query = select(func.count(Favorite.id)).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()

    offset = (page - 1) * page_size
    query = (
        select(
            News,
            Favorite.created_at.label("favorite_time"),
            Favorite.id.label("favorite_id"),
        )
        .join(Favorite)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()

    return total, rows


# 清空收藏列表
async def clear_favorite_list(db: AsyncSession, user_id: int):
    """
    清空收藏列表
    """
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0  # type: ignore
