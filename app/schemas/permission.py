from datetime import datetime
from app.schemas.common import RequestBaseModel, PageParamsRequestBaseModel, ResponseBaseModel


class PermissionCreate(RequestBaseModel):
    code: str
    name: str

class PermissionUpdate(RequestBaseModel):
    name: str

class PermissionList(ResponseBaseModel):
    id: int
    code: str
    name: str

class PermissionRead(ResponseBaseModel):
    id: int
    code: str
    name: str
    created_at: datetime
    updated_at: datetime

class PermissionPage(PermissionRead):
    pass

class PermissionPageQueryParams(PageParamsRequestBaseModel):
    name: str | None = None