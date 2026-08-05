from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from models.database import NewsBaseModel




# 新闻分类
class Category(NewsBaseModel):
    __tablename__ = "news_category"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="id"
    )
    name: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, comment="分类名称"
    )
    sort_order: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="排序"
    )

    def __repr__(self):
        return (
            f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"
        )


# 新闻列表
class News(NewsBaseModel):
    __tablename__ = "news"

    # 创建索引，提升查询效率
    __table_args__ = (
        Index("idx_news_category_id", "category_id"),
        Index("idx_publish_time", "publish_time"),
    )

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="新闻id"
    )
    title: Mapped[str] = mapped_column(
        String(255), nullable=False, comment="新闻标题"
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(500), comment="新闻简介"
    )
    content: Mapped[str] = mapped_column(
        String, nullable=False, comment="内容"
    )
    image: Mapped[Optional[str]] = mapped_column(
        String(255), comment="封面图片URL"
    )
    author: Mapped[Optional[str]] = mapped_column(
        String(50), comment="作者"
    )
    category_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("news_category.id"), nullable=False, comment="新闻分类ID"
    )
    views: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False, comment="浏览量"
    )
    publish_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, comment="发布时间"
    )

    def __repr__(self):
        return (
            f"<News(id={self.id}, title={self.title}, category_id={self.category_id}, publish_time={self.publish_time})>"
        )
