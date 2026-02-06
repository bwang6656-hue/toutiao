
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from models.history import History
from datetime import datetime

from models.news import News


# 添加浏览历史
async def add_history(db: AsyncSession, user_id: int, news_id: int):
    query = select(History).where(History.user_id == user_id, History.news_id == news_id)
    result = await db.execute(query)
    exist_history = result.scalar_one_or_none()
    if exist_history:
        exist_history.view_time = datetime.now()
        await db.commit()
        await db.refresh(exist_history)
        return exist_history
    else:
        history = History(user_id=user_id,news_id=news_id)
        db.add(history)
        await db.commit()
        await db.refresh(history)
        return history


# 获取浏览历史列表: 获取某个用户的浏览历史 + 分页
async def get_history_list(
        db: AsyncSession,
        user_id: int,
        page: int = 1,
        page_size: int = 100
):
    # 总量 + 浏览历史的浏览历史列表
    count_query = select(func.count(History.id)).where(History.user_id == user_id)
    count_result = await db.execute(count_query)
    total_count = count_result.scalar_one_or_none()
    # 获取浏览历史列表: 联表查询join() + 分页limit() + offset() + 浏览时间顺序
    query = (select(News, History.view_time.label("view_time"), History.id.label("history_id"))
             .join(History, History.news_id == News.id)
             .where(History.user_id == user_id)
             .order_by(History.view_time.desc())
             .offset((page-1) * page_size).limit(page_size)
             )
    result = await db.execute(query)
    rows = result.all()
    return rows,total_count


# 删除单条浏览记录
async def delete_history(db: AsyncSession, user_id: int, history_id: int
):
    stmt = delete(History).where(History.user_id == user_id, History.news_id == history_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount > 0


# 清空历史记录
async def clear_history(db: AsyncSession, user_id: int):
    stmt = delete(History).where(History.user_id == user_id)
    result = await db.execute(stmt)
    await db.commit()
    return result.rowcount or 0
