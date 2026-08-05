# database.py
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# 1. 定义全局唯一的声明式基类
class Base(DeclarativeBase):
    pass

# 2. 定义包含公共字段的抽象基类
class NewsBaseModel(Base):
    __abstract__ = True  # 关键：告诉 SQLAlchemy 不要为这个类创建真实的数据库表

    # 公共字段定义
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间"
    )
