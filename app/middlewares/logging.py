import time
import json
from fastapi import Request
from app.core.logger import logger


async def logging_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)

    duration = time.time() - start

    try:
        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        # ⚠️ 重新构造 response（关键）
        from starlette.responses import Response as StarletteResponse
        response = StarletteResponse(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type
        )

        data = json.loads(body.decode())
        code = data.get("code", 0)

        if code == 0:
            logger.info(
                f"{request.method} {request.url.path} "
                f"{duration:.3f}s"
            )
        else:
            logger.warning(
                f"{request.method} {request.url.path} "
                f"code={code} {duration:.3f}s"
            )

    except Exception:
        logger.warning(
            f"{request.method} {request.url.path}"
        )

    return response
