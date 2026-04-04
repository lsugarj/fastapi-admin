from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.response import ResponseModel, Response
from app.schemas.user import UserLogin, Token
from app.services import UserService


router = APIRouter(prefix="/public/user")


@router.post("/login", response_model=ResponseModel[Token])
async def login(
    params: UserLogin,
    session: AsyncSession = Depends(get_session),
):
    data = await UserService.login(params, session)
    return Response.success(data=data)
