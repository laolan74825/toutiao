from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

# 导入update
from config.db_config import get_db
from crud import favorite
from models.users import User
from schemas.favorite import (
    FavoriteAddRequest,
    FavoriteItemResponse,
    FavoriteNewsListResponse,
)
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/favorite", tags=["favorite"])


# 检查新闻是否已收藏
@router.get("/check")
async def check_favorite(
    news_id: int = Query(..., alias="newsId", description="新闻ID"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    检查新闻是否已收藏
    """
    is_favorite = await favorite.check_news_favorite(db, user.id, news_id)

    data = {"isFavorite": is_favorite}
    return success_response(message="检查收藏状态完成", data=data)


# 添加新闻收藏
@router.post("/add")
async def add_favorite(
    data: FavoriteAddRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    添加新闻收藏
    """
    result = await favorite.add_favorite(db, user.id, data.news_id)

    return success_response(message="添加收藏成功", data=result)


# 取消新闻收藏
@router.delete("/remove")
async def remove_favorite(
    news_id: int = Query(..., alias="newsId", description="新闻ID"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    取消新闻收藏
    """
    result = await favorite.remove_favorite(db, user.id, news_id)
    if not result:
        # 抛出异常
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="取消收藏失败"
        )
    return success_response(message="取消收藏成功")

# 获取收藏列表
@router.get("/list")
async def get_favorite_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, alias="pageSize", ge=1, le=100, title="每页数量"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    获取收藏列表
    """
    total, rows = await favorite.get_favorite_list(db, user.id, page, page_size)
    favorite_list = []
    for news, favorite_time, favorite_id in rows:
        news.favorite_time = favorite_time
        news.favorite_id = favorite_id
        favorite_list.append(FavoriteNewsListResponse.model_validate(news))
    has_more = (page * page_size) < total
    data = FavoriteItemResponse(list=favorite_list, total=total, hasMore=has_more)
    return success_response(message="获取收藏列表成功", data=data)


# 清空收藏列表
@router.delete("/clear")
async def clear_favorite_list(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    清空收藏列表
    """
    count = await favorite.clear_favorite_list(db, user.id)
    if not count == 0:
        # 抛出异常
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="清空收藏列表失败"
        )
    print("清空收藏列表成功")
    return success_response(message=f"清空{count}收藏列表成功",data=None)
