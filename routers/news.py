from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import news_cache as news

router = APIRouter(prefix="/api/news", tags=["news"])



# 获取新闻分类列表
@router.get("/categories")
async def get_categories(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    categories = await news.get_categories(db, skip, limit)
    return {"code": 200, "msg": "获取新闻分类列表成功", "data": categories}


# 获取新闻列表
@router.get("/list")
async def get_news(
    category_id: int = Query(..., alias="categoryId", title="新闻分类ID"),
    page: int = 1,
    page_size: int = Query(10, alias="pageSize", le=100, title="每页数量"),
    db: AsyncSession = Depends(get_db),
):

    offset = (page - 1) * page_size
    limit = page_size
    total = await news.get_news_total(db, category_id)
    news_list = await news.get_news_list(db, category_id, offset, limit)
    hasMore = total > (offset + len(news_list))
    return {
        "code": 200,
        "msg": "获取新闻列表成功",
        "data": {"list": news_list, "total": total, "hasMore": hasMore},
    }


# 获取新闻详情
@router.get("/detail")
async def get_news_detail(
    news_id: int = Query(..., alias="id", title="新闻ID"),
    db: AsyncSession = Depends(get_db),
):

    news_detail = await news.get_news_detail(db, news_id)

    if not news_detail:
        raise HTTPException(status_code=404, detail="新闻不存在")

    views_res = await news.update_news_views(db, news_detail.id)  # 更新浏览量

    if not views_res:
        raise HTTPException(status_code=500, detail="更新新闻浏览量失败")

    # 获取相关新闻
    related_news = await news.get_related_news(
        db, news_detail.id, news_detail.category_id
    )

    return {
        "code": 200,
        "msg": "获取新闻详情成功",
        "data": {
            "id": news_detail.id,
            "title": news_detail.title,
            "content": news_detail.content,
            "image": news_detail.image,
            "author": news_detail.author,
            "publish_time": news_detail.publish_time,
            "category_id": news_detail.category_id,
            "views": news_detail.views,
            "relatedNews": related_news,
        },
    }
