from starlette.requests import Request
from starlette.responses import Response


async def add_ok_response(request: Request, call_next):
    response: Response = await call_next(request)
    if 200 <= response.status_code <= 299:
        pass
