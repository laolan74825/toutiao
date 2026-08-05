from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field

from .base import NewsItemBase

class FavoriteCheckResponse(BaseModel):
    """收藏状态返回"""

    is_favorite: bool = Field(..., alias="isFavorite", description="是否已收藏")
    model_config = ConfigDict(
        populate_by_name=True,  # 通过名称填充 alias / 字段名兼容
    )


class FavoriteAddRequest(BaseModel):
    """收藏添加请求"""

    news_id: int = Field(..., alias="newsId", description="新闻ID")


class FavoriteAddResponse(BaseModel):
    """收藏添加返回"""

    id: int = Field(..., description="收藏ID")
    user_id: int = Field(..., alias="userId", description="用户ID")
    news_id: int = Field(..., alias="newsId", description="新闻ID")
    created_at: str = Field(..., alias="createdAt", description="收藏时间")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从ORM属性取值
    )


# 新联模型类
# 收藏新闻列表模型类
class FavoriteNewsListResponse(NewsItemBase):
    """收藏列表返回"""
    favorite_id: int = Field(..., alias="favoriteId", description="收藏ID")
    favorite_time: datetime = Field(..., alias="favoriteTime", description="收藏时间")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从ORM属性取值
        populate_by_name=True,  # 通过名称填充 alias / 字段名
    )



# 收藏列表接口响应模型
class FavoriteItemResponse(BaseModel):
    """收藏列表返回"""

    list: List[FavoriteNewsListResponse]
    total: int = Field(..., description="收藏总数")
    has_more: bool = Field(..., alias="hasMore")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从ORM属性取值
        populate_by_name=True,  # 通过名称填充 alias / 字段名兼容
    )
