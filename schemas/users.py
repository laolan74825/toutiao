
from pydantic import BaseModel, ConfigDict, Field


class UserRequest(BaseModel):
    username: str
    password: str


# 用户信息返回类：基础类 + 用户信息
class UserInfoBase(BaseModel):
    # 包括：昵称、头像URL、性别、个人简介
    nickname: str | None = Field(None, max_length=50, description="昵称")
    avatar: str | None = Field(None, max_length=255, description="头像URL")
    gender: str | None = Field(None, max_length=10, description="性别")
    bio: str | None = Field(None, max_length=500, description="个人简介")


class UserInfoResponse(UserInfoBase):
    id: int
    username: str
    model_config = ConfigDict(
        from_attributes=True,  # 允许从ORM属性取值
    )


class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="userInfo")

    # 模型配置
    model_config = ConfigDict(
        populate_by_name=True,  # 通过名称填充 alias / 字段名兼容
        from_attributes=True,  # 允许从ORM属性取值
    )

# 用户信息更新类：
class UserUpdateRequest(UserInfoBase):
    phone: str | None = Field(None, max_length=20, description="手机号")

# 修改用户密码类：
class UpdatePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., alias="newPassword", min_length=6, description="新密码")
