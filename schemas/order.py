from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Union
from user import User
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

class OrderBase(BaseModel):
    """订单基本信息模型"""
    shop_id: str = Field(..., max_length=50, description="店铺ID")
    order_number: str = Field(..., max_length=50, description="订单号")
    price: float = Field(..., description="价格")
    status: OrderStatus = Field(..., description="订单状态")
    audit_status: AuditStatus = Field(AuditStatus.UNAUDITED, description="审核状态")
    remark: Optional[str] = Field(None, max_length=255, description="备注")
    settlement_time: Optional[datetime] = Field(None, description="结算时间")
    payment_time: Optional[datetime] = Field(None, description="付款时间")
    shipping_time: Optional[datetime] = Field(None, description="发货时间")
    closing_time: Optional[datetime] = Field(None, description="关闭时间")
    confirmation_time: Optional[datetime] = Field(None, description="确认收货时间")
    is_bound: bool = Field(True, description="订单绑定状态")
    user_id: Optional[int] = Field(None, description="接单人ID")
    order_type: OrderType = Field(OrderType.TAOBAO, description="订单类型")

class OrderCreate(OrderBase):
    """创建订单模型"""
    pass

class OrderUpdate(OrderBase):
    """更新订单模型"""
    pass

class OrderInDBBase(OrderBase):
    """数据库中订单的基本模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Order(OrderInDBBase):
    """返回给客户端的订单模型"""
    user: Optional[User] = None

class OrderSearchParams(BaseModel):
    """订单搜索参数模型"""
    order_number: Optional[str] = Field(None, description="订单号")
    shop_id: Optional[str] = Field(None, description="店铺ID")
    price_gt: Optional[float] = Field(None, description="价格大于")
    price_lt: Optional[float] = Field(None, description="价格小于")
    order_type: Optional[OrderType] = Field(None, description="订单类型")
    is_bound: Optional[bool] = Field(True, description="订单绑定状态")
    status_exclude: Optional[List[OrderStatus]] = Field(None, description="订单状态不包含")
    status_include: Optional[List[OrderStatus]] = Field(None, description="订单状态包含")
    user_id: Optional[int] = Field(None, description="接单人ID")
    exclude_user_id: Optional[int] = Field(None, description="忽略接单人ID")
    group: Optional[str] = Field(None, description="组")
    order_time_start: Optional[datetime] = Field(None, description="下单时间开始")
    order_time_end: Optional[datetime] = Field(None, description="下单时间结束")
    payment_time_start: Optional[datetime] = Field(None, description="付款时间开始")
    payment_time_end: Optional[datetime] = Field(None, description="付款时间结束")
    shipping_time_start: Optional[datetime] = Field(None, description="发货时间开始")
    shipping_time_end: Optional[datetime] = Field(None, description="发货时间结束")
    closing_time_start: Optional[datetime] = Field(None, description="关闭时间开始")
    closing_time_end: Optional[datetime] = Field(None, description="关闭时间结束")
    confirmation_time_start: Optional[datetime] = Field(None, description="确认收货时间开始")
    confirmation_time_end: Optional[datetime] = Field(None, description="确认收货时间结束")
    audit_status: Optional[List[AuditStatus]] = Field(None, description="审核状态")