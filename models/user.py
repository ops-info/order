from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from base import Base

class User(Base):
    """用户表模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, comment="用户ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    password_hash = Column(String(100), nullable=False, comment="加密后的密码")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="邮箱")
    phone = Column(String(20), unique=True, index=True, nullable=True, comment="手机号")
    is_active = Column(Boolean, default=True, comment="账号是否启用")
    is_first_login = Column(Boolean, default=True, comment="是否首次登录")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 定义与订单表的关系
    orders = relationship("Order", back_populates="user")