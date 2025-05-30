from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from models import order as models
from schemas import order as schemas
from datetime import datetime

def get_order(db: Session, order_id: int):
    """根据订单ID获取订单信息"""
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def get_order_by_number(db: Session, order_number: str):
    """根据订单号获取订单信息"""
    return db.query(models.Order).filter(models.Order.order_number == order_number).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    """获取订单列表"""
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    """创建订单"""
    db_order = models.Order(
        shop_id=order.shop_id,
        order_number=order.order_number,
        price=order.price,
        status=order.status,
        audit_status=order.audit_status,
        remark=order.remark,
        settlement_time=order.settlement_time,
        payment_time=order.payment_time,
        shipping_time=order.shipping_time,
        closing_time=order.closing_time,
        confirmation_time=order.confirmation_time,
        is_bound=order.is_bound,
        user_id=order.user_id,
        order_type=order.order_type
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order: schemas.OrderUpdate):
    """更新订单信息"""
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        return None
    
    if order.shop_id:
        db_order.shop_id = order.shop_id
    if order.order_number:
        db_order.order_number = order.order_number
    if order.price is not None:
        db_order.price = order.price
    if order.status:
        db_order.status = order.status
    if order.audit_status:
        db_order.audit_status = order.audit_status
    if order.remark is not None:
        db_order.remark = order.remark
    if order.settlement_time is not None:
        db_order.settlement_time = order.settlement_time
    if order.payment_time is not None:
        db_order.payment_time = order.payment_time
    if order.shipping_time is not None:
        db_order.shipping_time = order.shipping_time
    if order.closing_time is not None:
        db_order.closing_time = order.closing_time
    if order.confirmation_time is not None:
        db_order.confirmation_time = order.confirmation_time
    if order.is_bound is not None:
        db_order.is_bound = order.is_bound
    if order.user_id is not None:
        db_order.user_id = order.user_id
    if order.order_type:
        db_order.order_type = order.order_type
    
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    """删除订单"""
    db_order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not db_order:
        return False
    
    db.delete(db_order)
    db.commit()
    return True

def search_orders(db: Session, params: schemas.OrderSearchParams, skip: int = 0, limit: int = 100):
    """搜索订单"""
    query = db.query(models.Order)
    
    # 构建查询条件
    conditions = []
    
    if params.order_number:
        conditions.append(models.Order.order_number.ilike(f"%{params.order_number}%"))
    
    if params.shop_id:
        conditions.append(models.Order.shop_id.ilike(f"%{params.shop_id}%"))
    
    if params.price_gt is not None:
        conditions.append(models.Order.price > params.price_gt)
    
    if params.price_lt is not None:
        conditions.append(models.Order.price < params.price_lt)
    
    if params.order_type:
        conditions.append(models.Order.order_type == params.order_type)
    
    if params.is_bound is not None:
        conditions.append(models.Order.is_bound == params.is_bound)
    
    if params.status_exclude:
        conditions.append(models.Order.status.notin_(params.status_exclude))
    
    if params.status_include:
        conditions.append(models.Order.status.in_(params.status_include))
    
    if params.user_id is not None:
        conditions.append(models.Order.user_id == params.user_id)
    
    if params.exclude_user_id is not None:
        conditions.append(models.Order.user_id != params.exclude_user_id)
    
    if params.order_time_start and params.order_time_end:
        # 假设下单时间使用 created_at 字段
        conditions.append(and_(
            models.Order.created_at >= params.order_time_start,
            models.Order.created_at <= params.order_time_end
        ))
    
    if params.payment_time_start and params.payment_time_end:
        conditions.append(and_(
            models.Order.payment_time >= params.payment_time_start,
            models.Order.payment_time <= params.payment_time_end
        ))
    
    if params.shipping_time_start and params.shipping_time_end:
        conditions.append(and_(
            models.Order.shipping_time >= params.shipping_time_start,
            models.Order.shipping_time <= params.shipping_time_end
        ))
    
    if params.closing_time_start and params.closing_time_end:
        conditions.append(and_(
            models.Order.closing_time >= params.closing_time_start,
            models.Order.closing_time <= params.closing_time_end
        ))
    
    if params.confirmation_time_start and params.confirmation_time_end:
        conditions.append(and_(
            models.Order.confirmation_time >= params.confirmation_time_start,
            models.Order.confirmation_time <= params.confirmation_time_end
        ))
    
    if params.audit_status:
        conditions.append(models.Order.audit_status.in_(params.audit_status))
    
    # 应用查询条件
    if conditions:
        query = query.filter(and_(*conditions))
    
    # 执行查询
    return query.offset(skip).limit(limit).all()