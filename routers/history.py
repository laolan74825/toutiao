from fastapi import Depends, APIRouter, HTTPException, status, Query
from models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from utils.auth import get_current_user
from utils.response import success_response
from schemas.history import HistoryAddRequest, HistoryAddResponse, HistoryItemResponse, HistoryListResponse
from crud import history

router = APIRouter(prefix="/api/history", tags=["history"])


@router.post("/add")
async def add_history(
    request: HistoryAddRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    try:
        result = await history.add_history(db, user.id, request.news_id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="该记录已存在")

        data = HistoryAddResponse.model_validate(result)
        print(data)
        return success_response(message="添加历史记录成功",data=data)

    except Exception as e:
        # 添加日志以便调试真正的 500 错误原因
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"添加历史记录失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="服务器内部错误")


@router.get("/list")
async def get_history_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100, alias="pageSize"),
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        offset = (page - 1) * page_size
        total, rows = await history.get_history_list(db, user.id, offset, page_size)
        if total == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="没有历史记录")
    except Exception as e:
        # 添加日志以便调试真正的 500 错误原因
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"获取历史记录失败: {str(e)}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="服务器内部错误")

    history_list = []
    for news, history_id, view_time in rows:
        news.history_id = history_id
        news.view_time = view_time
        history_list.append(HistoryListResponse.model_validate(news))

    hasMore = total > page * page_size
    data = HistoryItemResponse(list=history_list, hasMore=hasMore, total=total)
    return success_response(message="获取历史记录成功", data=data)


# 删除历史记录
@router.delete("/delete/{news_id}")
async def delete_history(
    news_id: int,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    isDel = await history.delete_history(db, user.id, news_id)
    if not isDel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="没有该历史记录")

    return success_response(message="删除历史记录成功", data=None)


# 清空历史记录
@router.delete("/clear")
async def clear_history(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    await history.clear_history(db, user.id)

    return success_response(message="清空历史记录成功", data=None)
