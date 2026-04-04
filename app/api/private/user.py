from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session, get_read_session
from app.core.deps import get_current_user
from app.core.response import ResponseModel, Response
from app.schemas.common import IDResult, PageResult, BoolResult
from app.schemas.user import UserCreate, UserRead, UserPageQueryParams, UserList, UserUpdate, CurrentUser, UserPage
from app.services.user_service import UserService
from fastapi import Request


router = APIRouter(prefix="/private/users", dependencies=[Depends(get_current_user)])


@router.post("", response_model=ResponseModel[IDResult])
async def create_user(
    params: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    result = await UserService.create_user(params, session)
    return Response.success(data=result)


@router.patch("/detail/{user_id}", response_model=ResponseModel[BoolResult])
async def update_user(
    user_id: int,
    params: UserUpdate,
    session: AsyncSession = Depends(get_session),
):
    data = await UserService.update_user(user_id, params, session)
    return Response.success(data=data)


@router.delete("/detail/{user_id}", response_model=ResponseModel[BoolResult])
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_session),
):
    data = await UserService.delete_user(user_id, session)
    return Response.success(data=data)


@router.get("/detail/{user_id}", response_model=ResponseModel[UserRead])
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_read_session),
):
    data = await UserService.get_user_by_id(user_id, session)
    return Response.success(data=data)


@router.get("/me", response_model=ResponseModel[CurrentUser])
async def get_me(request: Request):
    return Response.success(data=request.state.user)


@router.get("/list", response_model=ResponseModel[List[UserList]])
async def get_user_list(
    session: AsyncSession = Depends(get_read_session),
):
    page_result = await UserService.get_user_list(session)
    return Response.success(data=page_result)


@router.get("/pages", response_model=ResponseModel[PageResult[UserPage]])
async def get_user_page(
    params: UserPageQueryParams = Depends(),
    session: AsyncSession = Depends(get_read_session),
):
    page_result = await UserService.get_user_page(params, session)
    return Response.success(data=page_result)