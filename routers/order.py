from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import order as schemas
from crud import order as crud
from database import get_db
from typing import List
from user import get_current_user
from schemas.user import User

# 路由实例
router = APIRouter()

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """创建订单"""
    db_order = crud.get_order_by_number(db, order_number=order.order_number)
    if db_order:
        raise HTTPException(status_code=400, detail="订单号已存在")
    
    return crud.create_order(db=db, order=order)

@router.get("/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取订单列表"""
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@router.get("/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """获取单个订单"""
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="订单不存在")
    return db_order

@router.put("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    """更新订单信息"""
    db_order = crud.update_order(db, order_id=order_id, order=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="订单不存在")
    return db_order

@router.delete("/{order_id}", response_model=schemas.MessageResponse)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """删除订单"""
    success = crud.delete_order(db, order_id=order_id)
    if not success:
        raise HTTPException(status_code=404, detail="订单不存在")
    return {"message": "订单已删除"}

@router.post("/search", response_model=List[schemas.Order])
def search_orders(
    params: schemas.OrderSearchParams, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """搜索订单"""
    orders = crud.search_orders(db, params=params, skip=skip, limit=limit)
    return orders

@router.post("/{order_id}/assign", response_model=schemas.Order)
def assign_order_to_user(
    order_id: int, 
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """将订单分配给用户"""
    # 检查订单是否存在
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 检查用户是否存在
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 分配订单
    db_order.user_id = user_id
    db.commit()
    db.refresh(db_order)
    
    return db_order

@router.post("/{order_id}/ship", response_model=schemas.Order)
def ship_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """发货操作"""
    # 检查订单是否存在
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 检查订单状态是否允许发货
    if db_order.status != schemas.OrderStatus.WAITING_FOR_SHIPMENT:
        raise HTTPException(
            status_code=400, 
            detail=f"订单状态不允许发货，当前状态: {db_order.status}"
        )
    
    # 更新订单状态和发货时间
    db_order.status = schemas.OrderStatus.SHIPPED
    db_order.shipping_time = datetime.now()
    db_order.user_id = current_user.id  # 设置接单人
    
    db.commit()
    db.refresh(db_order)
    
    return db_order