from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class UserRequest(BaseModel):
    username: str
    password: str

class UserInfoBase(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像URL")
    gender: Optional[str] = Field(None, max_length=10, description="性别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")

# user_info数据类型
class UserInfoResponse(BaseModel):
    id:int
    username:str
    bio: Optional[str] = None
    avatar: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True, #从ORM属性中填充数据
    )
    

# data数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(..., alias="UserInfo")
    #模型类配置
    model_config = ConfigDict(
        populate_by_name=True, #别名跟字段名兼容
        from_attributes=True, #从ORM属性中填充数据
    )

# 修改用户信息请求体
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None

# 修改密码
class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(..., alias="oldPassword", description="旧密码")
    new_password: str = Field(..., min_length=6, alias="newPassword", description="新密码")
    
    model_config = ConfigDict(
        populate_by_name=True, # 支持通过别名填充数据
    )