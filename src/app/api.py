from typing import List, Optional
from fastapi import APIRouter
from starlette.responses import JSONResponse
from pydantic import BaseModel

from app.client.routes.client import router as client_router


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"ok": True}


api_router.include_router(client_router, prefix="/client", tags=["client"])
