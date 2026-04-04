from fastapi import Request, HTTPException, Depends
from app.core.security import decode_token
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.schemas.user import CurrentUser
from app.services import UserService


def _extract_token(request: Request) -> str:
    auth = request.headers.get("Authorization", "")
    if auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()
    return ""


# 基础：获取 user_id
def get_current_user_id(request: Request) -> int:
    token = _extract_token(request)

    if not token:
        raise HTTPException(status_code=401, detail="未登录")

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="token无效")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="token错误")

    return int(user_id)


# 核心依赖
async def get_current_user(
    request: Request,
    user_id: int = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_session),
) -> CurrentUser:
    # 请求级缓存
    if hasattr(request.state, "user"):
        return request.state.user
    user = await UserService.get_current_user(user_id, session)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    request.state.user = user
    return user


# =========================
# RBAC：角色控制
# =========================
def require_role(role: str):
    def checker(user: CurrentUser = Depends(get_current_user)):
        if role not in user.roles:
            raise HTTPException(
                status_code=403,
                detail=f"需要角色: {role}",
            )
        return user

    return checker


# =========================
# RBAC：权限控制
# =========================
def require_permission(permission: str):
    def checker(user: CurrentUser = Depends(get_current_user)):
        if permission not in user.permissions:
            raise HTTPException(
                status_code=403,
                detail=f"需要权限: {permission}",
            )
        return user

    return checker