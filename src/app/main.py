import uvicorn
import time
import logging
from fastapi import status
from fastapi import FastAPI
from starlette.middleware.base import RequestResponseEndpoint
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.api import api_router
from app.exceptions import exception_handlers, limiter
from app.settings import settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title="client",
    description="client",
    exception_handlers=exception_handlers,
    limiter=limiter,
)


@app.middleware("http")
async def metrics_middleware(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    request_path = getattr(request, "path", request.url.path)
    path_template = ".".join(request_path.split("/")[1:])

    start_time = time.time()
    response = await call_next(request)
    elapsed_time = time.time() - start_time
    logger.debug(f"server.call.elapsed.{path_template}: {elapsed_time}")
    return response


@app.middleware("http")
async def exception_middleware(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    try:
        response = await call_next(request)
    except ValidationError as e:
        logger.exception(e)
        response = JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": e.errors()},
        )
    except ValueError as e:
        logger.exception(e)
        response = JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": [{"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]
            },
        )
    except Exception as e:
        logger.exception(e)
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": [{"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]
            },
        )
    return response


app.add_middleware(
    CORSMiddleware,
    allow_credentials=settings.cors.allow_credentials,
    allow_origins=settings.cors.allow_origins,
    allow_headers=settings.cors.allow_headers,
    allow_methods=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.api.host, port=settings.api.port, reload=True)
