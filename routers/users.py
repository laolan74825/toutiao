from fastapi import APIRouter, Depends, HTTPException, status
from models.users import User
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud import users
from schemas.users import UserAuthResponse, UserInfoResponse, UserRequest
from schemas.users import UserUpdateRequest, UpdatePasswordRequest
from utils.response import success_response
from utils.auth import get_current_user

router = APIRouter(prefix="/api/user", tags=["users"])


# 用户注册
@router.post("/register")
async def register_user(user_data: UserRequest, db: AsyncSession = Depends(get_db)):

    # 检查用户名是否已存在
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在"
        )

    user = await users.create_user(db, user_data)
    user_token = await users.create_token(db, user.id)

    response_data = UserAuthResponse(
        token=user_token.token,
        userInfo=UserInfoResponse.model_validate(user),
    )

    return success_response(message="注册成功", data=response_data)
    # return {
    #     "code": 200,
    #     "message": "注册成功",
    #     "data": {
    #         "token": user_token.token,
    #         "userInfo": {
    #             "id": user.id,
    #             "username": user.username,
    #             "bio": user.bio,
    #             "avatar": user.avatar,
    #         },
    #     },
    # }


# 用户登录
@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):

    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误"
        )

    # 生成Token
    user_token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(
        token=user_token.token,
        userInfo=UserInfoResponse.model_validate(user),
    )
    return success_response(message="登录成功", data=response_data)


# 用户信息
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    data = UserInfoResponse.model_validate(user)
    return success_response(message="获取用户信息成功", data=data)

# 修改用户信息
@router.put("/update")
async def update_user_info(
    user_data: UserUpdateRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    updated_user = await users.update_user(db, user.username, user_data)
    data = UserInfoResponse.model_validate(updated_user)
    return success_response(message="更新用户信息成功", data=data)


# 修改密码
@router.put("/password")
async def update_password(
    password_data: UpdatePasswordRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    res_chang_pwd = await users.update_user_password(db, user, password_data)
    if not res_chang_pwd:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="密码修改失败！"
        )
    return success_response(message="密码修改成功")
