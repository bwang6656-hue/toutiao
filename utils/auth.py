#根据token查询用户并返回用户
from fastapi import Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud.users import get_user_info_by_token


async def get_current_user(
    authorizer: str = Header(..., alias="Authorization"),
    db: AsyncSession = Depends(get_db), 
    ):
    user = await get_user_info_by_token(db, authorizer)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user