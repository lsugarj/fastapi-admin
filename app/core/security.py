from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 验证密码
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# 密码加密
def hash_password(password: str):
    return pwd_context.hash(password)

# 生成 JWT
def create_access_token(data: dict):
    secret_config = get_settings().secret
    to_encode = data.copy()
    if "sub" in to_encode and to_encode["sub"] is not None and not isinstance(to_encode["sub"], str):
        to_encode["sub"] = str(to_encode["sub"])
    expire = datetime.now(UTC) + timedelta(minutes=secret_config.access_token_expires)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_config.secret_key, algorithm=secret_config.algorithm)

# 解析 JWT
def decode_token(token: str):
    secret_config = get_settings().secret
    try:
        return jwt.decode(
            token, secret_config.secret_key, algorithms=[secret_config.algorithm]
        )
    except JWTError:
        return None
