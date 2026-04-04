from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import HTTPException as FastAPIHTTPException
from app.core.response import Response
from app.exceptions.codes import Code
from app.utils.validation import format_validation_errors
from app.exceptions.business import BusinessException
from app.core.logger import logger


def register_exception_handlers(app):

    # =========================
    # 参数异常
    # =========================
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = format_validation_errors(exc)

        logger.warning(
            "[VALIDATION_ERROR] method=%s path=%s errors=%s",
            request.method,
            request.url.path,
            errors,
        )

        return JSONResponse(
            status_code=422,
            content=Response.fail(
                code=Code.VALIDATION_ERROR,
                message="参数校验失败",
                error=errors
            ).model_dump()
        )

    # =========================
    # 业务异常
    # =========================
    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        logger.warning(
            "[BUSINESS_ERROR] method=%s path=%s code=%s msg=%s",
            request.method,
            request.url.path,
            exc.code,
            exc.message,
        )

        return JSONResponse(
            status_code=200,
            content=Response.fail(
                code=exc.code,
                message=exc.message
            ).model_dump()
        )

    # =========================
    # HTTP异常（含404）
    # =========================
    @app.exception_handler(StarletteHTTPException)
    @app.exception_handler(FastAPIHTTPException)
    async def http_exception_handler(request: Request, exc):
        if exc.status_code == 404:
            code = Code.ROUTE_NOT_FOUND
            message = "Resource not found"

        elif exc.status_code == 401:
            code = Code.NO_LOGIN
            message = exc.detail

        elif exc.status_code == 403:
            code = Code.NO_PERMISSION
            message = exc.detail

        else:
            code = exc.status_code
            message = exc.detail

        logger.warning(
            "[HTTP_ERROR] method=%s path=%s status=%s detail=%s",
            request.method,
            request.url.path,
            exc.status_code,
            exc.detail,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=Response.fail(
                code=code,   # 可按你们规范定义
                message=message
            ).model_dump()
        )

    # =========================
    # 系统异常（兜底）
    # =========================
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc):
        # ✅ 唯一一条系统异常日志（必须带堆栈）
        logger.exception(
            "[SYSTEM_ERROR] method=%s path=%s query=%s",
            request.method,
            request.url.path,
            request.url.query,
        )

        return JSONResponse(
            status_code=500,
            content=Response.fail(
                code=50000,
                message="服务器内部错误"
            ).model_dump()
        )