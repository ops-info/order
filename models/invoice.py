from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Invoice(Base):
    """发票表模型"""
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True, comment="发票ID")
    invoice_number = Column(String(50), unique=True, index=True, nullable=False, comment="发票号")
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, comment="关联订单ID")
    amount = Column(Float, nullable=False, comment="金额")
    invoice_type = Column(String(50), nullable=False, comment="发票类型")
    issuing_date = Column(DateTime, nullable=False, comment="开票日期")
    remark = Column(String(255), nullable=True, comment="备注")
    
    # 关联订单表
    order = relationship("Order", backref="invoices")
    
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")