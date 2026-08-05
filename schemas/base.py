# 导入BaseModel
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

class NewsItemBase(BaseModel):
    """新闻列表项"""
    id: int
    title: str
    description: str | None = None
    image: str | None = None
    author: str | None = None
    category_id: int = Field(..., alias="categoryId")
    views: int
    publish_time: datetime | None = Field(None, alias="publishTime")

    model_config = ConfigDict(
        from_attributes=True,  # 允许从ORM属性取值
        populate_by_name=True,  # 通过名称填充 alias / 字段名兼容
    )
