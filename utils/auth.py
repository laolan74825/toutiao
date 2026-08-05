# 整合 根据Token 获取用户信息
from fastapi import HTTPException, Header, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud.users import get_user_by_token


async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),
        db: AsyncSession = Depends(get_db)
):
    token = authorization.removeprefix("Bearer ").strip()
    user = await get_user_by_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的Token或Token已过期"
            )
    return user
