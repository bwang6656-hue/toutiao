from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from models.news import Category, News

async def get_categories(db:AsyncSession, skip=0, limit=100):
    stmt = select(Category).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

#列表查询
async def get_news_list(db:AsyncSession,category_id:int, skip:int=0, limit:int=10):
    #查询指定分类下的所有新闻
    stmt = select(News).where(News.category_id == category_id).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

#获取新闻总量
async def get_news_count(db:AsyncSession, category_id:int):
    # 查询指定分类下新闻数量
    stmt = select(func.count(News.id)).where(News.category_id == category_id)
    result = await db.execute(stmt)
    return result.scalar_one()#只能有一个结果，否则报错

#获取新闻详情
async def get_news_detail(db:AsyncSession, news_id:int):
    stmt = select(News).where(News.id == news_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

#增加浏览量
async def increase_news_views(db:AsyncSession, news_id:int):
    stmt = update(News).where(News.id == news_id).values(views=News.views + 1)
    result = await db.execute(stmt)
    await db.commit()
    #检查数据库是否真的命中了数据-> 命中了返回True
    return result.rowcount > 0 if hasattr(result, "rowcount") else True

#获取同类新闻
async def get_related_news(db:AsyncSession, news_id:int, category_id:int, limit:int=5):
    # 查询指定分类下的所有新闻,orderBy浏览量和发布时间排序, 排除当前新闻
    stmt = select(News).where(
        News.category_id == category_id, News.id != news_id
        ).order_by(News.views.desc(), News.publish_time.desc()).limit(limit)
    result = await db.execute(stmt)
    #return result.scalars().all()
    related_news = result.scalars().all()
    #列表推导式，推导新闻的核心数据再return
    related_news_data = [
        {
            "id": news.id,
            "title": news.title,
            "views": news.views,
            "publishTime": news.publish_time,
            "categoryId": news.category_id,
            "image": news.image,
            "author": news.author,
            "content": news.content,
        }
        for news in related_news
    ]
    return related_news_data
