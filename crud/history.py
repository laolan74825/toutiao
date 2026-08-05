from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.history import History
from models.news import News

# 检查历史记录是否存在
async def check_history(db: AsyncSession, user_id: int, news_id: int):
    query = select(History).where(
        History.news_id == news_id, History.user_id == user_id
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()

async def add_history(db: AsyncSession, user_id: int, news_id: int):
    # 检查历史记录是否已存在
    result = await check_history(db, user_id, news_id)

    if result is not None:
        return None

    history = History(user_id=user_id, news_id=news_id)
    db.add(history)
    await db.commit()
    await db.refresh(history)
    return history


async def get_history_list(db: AsyncSession, user_id: int, offset: int, page_size: int):
    # 获取总记录数
    total_query = select(func.count(History.id)).where(History.user_id == user_id)
    result = await db.execute(total_query)
    total = result.scalar_one()

    query = (
        select(News, History.id.label("history_id"), History.view_time)
        .join(History, History.news_id == News.id)
        .where(History.user_id == user_id)
        .order_by(History.view_time.desc())
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(query)
    rows = result.all()
    return total, rows


# 删除历史记录
async def delete_history(db: AsyncSession, user_id: int, news_id: int):
    query = delete(History).where(History.news_id == news_id, History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount > 0 # type: ignore

async def clear_history(db: AsyncSession, user_id: int):
    query = delete(History).where(History.user_id == user_id)
    result = await db.execute(query)
    await db.commit()

    return result.rowcount or 0 # type: ignore
