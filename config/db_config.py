from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# 数据库连接信息
ASYNC_DB_URL = "mysql+aiomysql://root:314159lgz@localhost:3306/news_app?charset=utf8mb4"

# # 创建异步数据库引擎
async_engine = create_async_engine(
    ASYNC_DB_URL,
    echo=True,  # 打印SQL语句
    pool_size=10,  # 连接池大小
    max_overflow=20,  # 连接池溢出时最大连接数
)

# 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    expire_on_commit=False,  # 提交时关闭会话
)


# 依赖项：获取异步数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:  # 创建异步会话
        try:
            yield session  # 返回异步会话
        except Exception:  # 捕获异常
            await session.rollback()  # 回滚事务
            raise  # 抛出异常
        finally:
            await session.close()  # 关闭会话
