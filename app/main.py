from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.public.user import router as public_user_router
from app.api.private.user import router as private_user_router
from app.api.private.permission import router as private_permission_router
from app.core.database import init_engine, close_engine
from app.core.redis import RedisClient
from app.exceptions.handlers import register_exception_handlers
from app.core.logger import setup_logger, logger
from app.middlewares.trace import trace_middleware
from app.middlewares.logging import logging_middleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ===== 启动阶段 =====
    setup_logger()
    logger.info("日志初始化成功")
    await init_engine()
    logger.info("数据库初始化成功")
    await RedisClient.init()
    logger.info("redis初始化成功")

    yield

    # ===== 关闭阶段 =====
    await close_engine()
    logger.info("数据库关闭成功")
    await RedisClient.close()
    logger.info("redis关闭成功")

app = FastAPI(lifespan=lifespan)
# 顺序非常关键（谁先执行）
app.middleware("http")(logging_middleware)
app.middleware("http")(trace_middleware)
# 注册异常处理
register_exception_handlers(app)
# 注册路由
app.include_router(public_user_router, prefix="/api")
app.include_router(private_user_router, prefix="/api")
app.include_router(private_permission_router, prefix="/api")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}
