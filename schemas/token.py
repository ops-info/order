# schemas/token.py
from pydantic import BaseModel

class Token(BaseModel):
    """JWT Token 模型"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token 数据模型"""
    username: str | None = None