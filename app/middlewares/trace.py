from fastapi import Request
from app.utils.context import set_trace_id

TRACE_HEADER = "X-Trace-Id"


async def trace_middleware(request: Request, call_next):
    trace_id = request.headers.get(TRACE_HEADER)

    trace_id = set_trace_id(trace_id)

    # 👉 放到 request.state（保险）
    request.state.trace_id = trace_id

    response = await call_next(request)
    response.headers[TRACE_HEADER] = trace_id

    return response