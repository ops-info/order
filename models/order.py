from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base
import enum

class OrderStatus(str, enum.Enum):
    """订单状态枚举类"""
    WAITING_FOR_SHIPMENT = "买家已付款等待发货"
    CLOSED = "交易关闭"
    SUCCESS = "交易成功"
    PARTIAL_REFUND = "部分退款"
    SHIPPED = "卖家已发货等待买家确认"

class AuditStatus(str, enum.Enum):
    """审核状态枚举类"""
    UNAUDITED = "未审核"
    AUDITED = "已审核"
    SETTLED = "已结算"
    UNSETTLED = "未结算"

class OrderType(str, enum.Enum):
    """订单类型枚举类"""
    TAOBAO = "淘宝网"

class Order(Base):
    """订单表模型"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, comment="订单ID")
    shop_id = Column(String(50), index=True, nullable=False, comment="店铺ID")
    order_number = Column(String(50), unique=True, index=True, nullable=False, comment="订单号")
    price = Column(Float, nullable=False, comment="价格")
    status = Column(Enum(OrderStatus), nullable=False, comment="订单状态")
    audit_status = Column(Enum(AuditStatus), default=AuditStatus.UNAUDITED, comment="审核状态")
    remark = Column(String(255), nullable=True, comment="备注")
    settlement_time = Column(DateTime, nullable=True, comment="结算时间")
    payment_time = Column(DateTime, nullable=True, comment="付款时间")
    shipping_time = Column(DateTime, nullable=True, comment="发货时间")
    closing_time = Column(DateTime, nullable=True, comment="关闭时间")
    confirmation_time = Column(DateTime, nullable=True, comment="确认收货时间")
    is_bound = Column(Boolean, default=True, comment="订单绑定状态")
    
    # 关联用户表
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, comment="接单人ID")
    user = relationship("User", back_populates="orders")
    
    # 订单类型
    order_type = Column(Enum(OrderType), default=OrderType.TAOBAO, comment="订单类型")
    
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")