from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import invoice as schemas
from crud import invoice as crud
from database import get_db
from typing import List

# 路由实例
router = APIRouter()

@router.post("/", response_model=schemas.Invoice)
def create_invoice(invoice: schemas.InvoiceCreate, db: Session = Depends(get_db)):
    """创建发票"""
    db_invoice = crud.get_invoice_by_number(db, invoice_number=invoice.invoice_number)
    if db_invoice:
        raise HTTPException(status_code=400, detail="发票号已存在")
    
    # 检查订单是否存在
    db_order = crud.get_order(db, order_id=invoice.order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="关联的订单不存在")
    
    return crud.create_invoice(db=db, invoice=invoice)

@router.get("/", response_model=List[schemas.Invoice])
def read_invoices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取发票列表"""
    invoices = crud.get_invoices(db, skip=skip, limit=limit)
    return invoices

@router.get("/{invoice_id}", response_model=schemas.Invoice)
def read_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """获取单个发票"""
    db_invoice = crud.get_invoice(db, invoice_id=invoice_id)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="发票不存在")
    return db_invoice

@router.put("/{invoice_id}", response_model=schemas.Invoice)
def update_invoice(invoice_id: int, invoice: schemas.InvoiceUpdate, db: Session = Depends(get_db)):
    """更新发票信息"""
    db_invoice = crud.update_invoice(db, invoice_id=invoice_id, invoice=invoice)
    if db_invoice is None:
        raise HTTPException(status_code=404, detail="发票不存在")
    return db_invoice

@router.delete("/{invoice_id}", response_model=schemas.MessageResponse)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)):
    """删除发票"""
    success = crud.delete_invoice(db, invoice_id=invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="发票不存在")
    return {"message": "发票已删除"}