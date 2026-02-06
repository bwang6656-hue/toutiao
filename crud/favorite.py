from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func

from models.favorite import Favorite, News


# 检查收藏状态: 当前用户是否收藏了这一条新闻
async def is_news_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    query = select(Favorite).where(Favorite.user_id == user_id, Favorite.news_id == news_id)
    result = await db.execute(query)
    # 是否有收藏记录
    return result.scalar_one_or_none() is not None

# 添加收藏
async def add_news_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    favorite = Favorite(news_id=news_id, user_id=user_id)
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

# 取消收藏
async def remove_news_favorite(
        db: AsyncSession,
        user_id: int,
        news_id: int
):
    # 先检查是否存在收藏记录
    exists_query = select(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user_id)
    exists_result = await db.execute(exists_query)
    if not exists_result.scalar_one_or_none():
        return False
    
    # 执行删除操作
    stmt = delete(Favorite).where(Favorite.news_id == news_id, Favorite.user_id == user_id)
    await db.execute(stmt)
    await db.commit()
    return True

# 获取收藏列表: 获取的是某个用户的收藏列表 + 分页功能
async def get_favorite_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 100
):
    #总量 + 收藏 的新闻列表
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_query)
    total_count = count_result.scalar_one
    #获取收藏列表: 联表查询join() + 分页limit() + offset() + 收藏时间顺序
    #select(查询主体模型类, 字段别名).join(联合查询的模型类，联合查询的条件).where().order_by().offset().limit()
    query = (select(News, Favorite.created_at.label("favorite_time"), Favorite.id.label("favorite_id"))
             .join(Favorite, Favorite.news_id==News.id).order_by(Favorite.news_id)
             .where(Favorite.user_id == user_id)
             .order_by(Favorite.created_at.desc())
             .offset((page-1) * page_size).limit(page_size)
             )
    result = await db.execute(query)
    rows = result.all()
    return rows,total_count

#清空当前用户收藏列表
async def remove_all_favorites(
        db: AsyncSession,
        user_id: int
):
    # 先查询用户的收藏数量
    count_query = select(func.count()).where(Favorite.user_id == user_id)
    count_result = await db.execute(count_query)
    total_count = count_result.scalar_one()
    
    # 执行删除操作
    stmt = delete(Favorite).where(Favorite.user_id == user_id)
    await db.execute(stmt)
    await db.commit()
    
    return total_count
