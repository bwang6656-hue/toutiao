import redis.asyncio as redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# 创建 Redis 连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,#redis服务器主机地址
    port=REDIS_PORT,#redis服务器端口号
    db=REDIS_DB,#redis数据库索引，默认为0
    decode_responses=True#是否将字节响应解码为字符串，默认为False
)