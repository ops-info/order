from sqlalchemy.orm import Session
from models import invoice as models
from schemas import invoice as schemas

def get_invoice(db: Session, invoice_id: int):
    """根据发票ID获取发票信息"""
    return db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()

def get_invoice_by_number(db: Session, invoice_number: str):
    """根据发票号获取发票信息"""
    return db.query(models.Invoice).filter(models.Invoice.invoice_number == invoice_number).first()

def get_invoices(db: Session, skip: int = 0, limit: int = 100):
    """获取发票列表"""
    return db.query(models.Invoice).offset(skip).limit(limit).all()

def create_invoice(db: Session, invoice: schemas.InvoiceCreate):
    """创建发票"""
    db_invoice = models.Invoice(
        invoice_number=invoice.invoice_number,
        order_id=invoice.order_id,
        amount=invoice.amount,
        invoice_type=invoice.invoice_type,
        issuing_date=invoice.issuing_date,
        remark=invoice.remark
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def update_invoice(db: Session, invoice_id: int, invoice: schemas.InvoiceUpdate):
    """更新发票信息"""
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not db_invoice:
        return None
    
    if invoice.invoice_number:
        db_invoice.invoice_number = invoice.invoice_number
    if invoice.order_id:
        db_invoice.order_id = invoice.order_id
    if invoice.amount is not None:
        db_invoice.amount = invoice.amount
    if invoice.invoice_type:
        db_invoice.invoice_type = invoice.invoice_type
    if invoice.issuing_date:
        db_invoice.issuing_date = invoice.issuing_date
    if invoice.remark is not None:
        db_invoice.remark = invoice.remark
    
    db.commit()
    db.refresh(db_invoice)
    return db_invoice

def delete_invoice(db: Session, invoice_id: int):
    """删除发票"""
    db_invoice = db.query(models.Invoice).filter(models.Invoice.id == invoice_id).first()
    if not db_invoice:
        return False
    
    db.delete(db_invoice)
    db.commit()
    return True