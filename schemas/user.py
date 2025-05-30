from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """用户基本信息模型"""
    username: str = Field(..., max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    is_active: bool = Field(True, description="账号是否启用")

class UserCreate(UserBase):
    """创建用户模型"""
    password: str = Field(..., min_length=8, description="密码")

class UserUpdate(UserBase):
    """更新用户模型"""
    password: Optional[str] = Field(None, min_length=8, description="密码")
    is_first_login: Optional[bool] = Field(None, description="是否首次登录")

class UserInDBBase(UserBase):
    """数据库中用户的基本模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class User(UserInDBBase):
    """返回给客户端的用户模型"""
    pass

class UserLogin(BaseModel):
    """用户登录模型"""
    username: str = Field(..., max_length=50, description="用户名")
    password: str = Field(..., min_length=8, description="密码")
    captcha: str = Field(..., max_length=6, description="验证码")

class UserChangePassword(BaseModel):
    """用户修改密码模型"""
    old_password: str = Field(..., min_length=8, description="旧密码")
    new_password: str = Field(..., min_length=8, description="新密码")