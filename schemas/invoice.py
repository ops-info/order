from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from order import Order

class InvoiceBase(BaseModel):
    """发票基本信息模型"""
    invoice_number: str = Field(..., max_length=50, description="发票号")
    order_id: int = Field(..., description="关联订单ID")
    amount: float = Field(..., description="金额")
    invoice_type: str = Field(..., max_length=50, description="发票类型")
    issuing_date: datetime = Field(..., description="开票日期")
    remark: Optional[str] = Field(None, max_length=255, description="备注")

class InvoiceCreate(InvoiceBase):
    """创建发票模型"""
    pass

class InvoiceUpdate(InvoiceBase):
    """更新发票模型"""
    pass

class InvoiceInDBBase(InvoiceBase):
    """数据库中发票的基本模型"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Invoice(InvoiceInDBBase):
    """返回给客户端的发票模型"""
    order: Optional[Order] = None