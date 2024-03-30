from fastapi import status
from fastapi import Depends, APIRouter
from app.database import db_session, Session
from app.authentication import authorization_token, Token
from app.client import service
from app.client.schemas.team import FindTeamsOut

router = APIRouter()


@router.post("/find-teams", status_code=status.HTTP_200_OK, response_model=FindTeamsOut)
async def find_teams(
    db: Session = Depends(db_session), token: Token = Depends(authorization_token)
):
    results = await service.find_teams(db, auth_id=token.auth_id)
    response = FindTeamsOut(ok=True, has_valid_cookie=True, **results)
    return response.model_dump()


@router.post("/boot")
async def boot(db: Session = Depends(db_session), token=Depends(authorization_token)):
    boot_data = await service.boot_client(db, **token.model_dump())
    return boot_data
