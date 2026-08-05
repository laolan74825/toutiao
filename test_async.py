import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


async def test():
    # 根据你的数据库修改 URL
    # SQLite: sqlite+aiosqlite:///test.db
    # PostgreSQL: postgresql+asyncpg://user:pass@localhost/db
    # MySQL: mysql+aiomysql://root:123456@localhost:3306/test

    engine = create_async_engine(
        "mysql+aiomysql://root:314159lgz@localhost:3306/news_app"
    )
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 'Hello, Async SQLAlchemy!'"))
        print(result.scalar())
    await engine.dispose()


asyncio.run(test())
