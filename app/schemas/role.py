from app.schemas.common import RequestBaseModel


class RoleCreate(RequestBaseModel):
    code: str
    name: str

class RoleRead(RoleCreate):
    id: int