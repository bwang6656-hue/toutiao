from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from schemas.users import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest,UserChangePasswordRequest
from crud import users
from starlette import status
from utils.response import success_response
from utils.auth import get_current_user
from models.users import User

router = APIRouter(prefix="/api/user", tags=["users"])

@router.post("/register")
async def register(user_data:UserRequest, db:AsyncSession = Depends(get_db)):#用户信息和数据库依赖注入
    # 1. 校验用户名是否已存在
    # 2. 密码加密存储
    # 3. 创建用户记录
    # 4. 生成用户访问令牌Token
    # 5. 返回用户信息和令牌响应结果
    existing_user = await users.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    user = await users.create_user(db, user_data)
    token = await users.create_token(db, user.id)
    # return {
    #     "code": 200,
    #     "message": "用户注册成功",
    #     "data": {
    #         "token":token,
    #         "user_info":{
    #             "id": user.id,
    #             "username":user.username,
    #             "bio":user.bio,
    #             "avatar":user.avatar
    #         }
    #     }
    # }
    response_data = UserAuthResponse(
        token=token,
        UserInfo=UserInfoResponse.model_validate(user),
    )
    return success_response(message="用户注册成功", data=response_data)

@router.post("/login")
async def login(user_data:UserRequest, db:AsyncSession = Depends(get_db)):
    #登录逻辑:
    # 1. 校验用户名是否存在
    # 2. 校验密码是否正确
    # 3. 生成用户访问令牌Token
    # 4. 返回用户信息和令牌响应结果
    user = await users.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db, user.id)
    response_data = UserAuthResponse(
        token=token,
        UserInfo=UserInfoResponse.model_validate(user),
    )
    return success_response(message="用户登录成功", data=response_data)

#获取用户信息:
# 1. 查Token对应的用户信息
# 2. 封装crud
# 3. 功能整合成一个工具函数
# 4. 路由导入使用
@router.get("/info")
async def get_user_info(user:User = Depends(get_current_user)):
    return success_response(message="用户信息获取成功", data=UserInfoResponse.model_validate(user))

# 修改用户信息:验证token，更新用户信息（用户名、密码、个人介绍、头像），定义pydantic模型，响应结果
@router.put("/update")
async def update_user_info(user_update:UserUpdateRequest, db:AsyncSession = Depends(get_db), current_user:User = Depends(get_current_user)):
    # 1. 校验用户是否存在
    # 2. 更新用户信息
    # 3. 返回更新后的用户信息
    user = await users.get_user_by_username(db, current_user.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    user = await users.update_user(db, current_user.username, user_update)
    return success_response(message="用户信息更新成功", data=UserInfoResponse.model_validate(user))

@router.put("/password")
async def update_password(
        password_data:UserChangePasswordRequest,
        user: User = Depends(get_current_user),
        db:AsyncSession = Depends(get_db)):
    res_change_pwd = await users.change_password(db, user, password_data.old_password, password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="修改密码失败，请稍后再试")
    return success_response(message="修改密码成功")