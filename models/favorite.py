from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base




class Favorite(Base):
    """
    收藏表ORM
    """

    __tablename__ = "favorite"

    # 创建索引，提升查询效率
    __table_args__ = (
        UniqueConstraint("user_id", "news_id", name="user_news_unique"),
        Index("fk_favorite_user_idx", "user_id"),
        Index("fk_favorite_news_idx", "news_id"),
    )

    # ID/user_id/news_id/created_at
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, comment="收藏ID"
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id"), nullable=False, comment="用户ID"
    )
    news_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("news.id"), nullable=False, comment="新闻ID"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False, comment="收藏时间"
    )

    def __repr__(self):
        return f"Favorite(id={self.id}, user_id={self.user_id}, news_id={self.news_id}, created_at={self.created_at})"
