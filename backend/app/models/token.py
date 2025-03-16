from pydantic import BaseModel


class Token(BaseModel):
    """访问令牌模型"""
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """JWT token的payload模型"""
    sub: str | None = None
    exp: int | None = None