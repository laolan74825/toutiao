from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import List
from schemas.base import NewsItemBase

class HistoryAddRequest(BaseModel):
    news_id: int = Field(..., alias="newsId")


class HistoryAddResponse(BaseModel):
    id: int = Field(..., description="历史记录ID")
    user_id: int = Field(..., alias="userId", description="用户ID")
    news_id: int = Field(..., alias="newsId", description="新闻ID")
    view_time: datetime = Field(..., alias="viewTime", description="浏览时间")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从ORM属性取值
        populate_by_name=True,  # 通过名称填充 alias / 字段名兼容
    )

class HistoryListResponse(NewsItemBase):
    # id/title/description/image/author/publish_time/category_id/views/view_time
    history_id: int = Field(..., description="新闻ID", alias="historyId")
    view_time: datetime = Field(..., alias="viewTime", description="浏览时间")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从ORM属性取值
        populate_by_name=True,  # 通过名称填充 alias / 字段名兼容
    )

class HistoryItemResponse(BaseModel):
    has_more: bool = Field(..., alias="hasMore")
    list: List[HistoryListResponse]
    total: int = Field(..., description="收藏总数")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从ORM属性取值
        populate_by_name=True,  # 通过名称填充 alias / 字段名兼容
    )
