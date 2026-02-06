from fastapi import FastAPI
from routers import news, users, favorite, history
from fastapi.middleware.cors import CORSMiddleware
from config.db_conf import async_engine
from utils.exception_handlers import register_exception_handlers


async def lifespan(app: FastAPI):
    yield
    await async_engine.dispose()

# 2. 创建FastAPI应用并绑定生命周期函数（核心步骤）
app = FastAPI(lifespan=lifespan)

#注册异常处理器
register_exception_handlers(app)

# 3. 原有CORS中间件配置：完全保留，无需修改
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许的源
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],  # 允许的请求方法
    allow_headers=["*"],  # 允许的请求头
)

# 4. 原有根接口：完全保留，无需修改
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 5. 原有路由注册：完全保留，无需修改
app.include_router(news.router)
app.include_router(users.router)
app.include_router(favorite.router)
app.include_router(history.router)