from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import invoice, order, user
from database import SessionLocal, engine
from routers import user, order, invoice

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

# 创建FastAPI应用实例
app = FastAPI(
    title="订单管理系统",
    description="用于对接淘宝网订单的管理系统",
    version="1.0.0",
)

# 配置CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 注册路由
app.include_router(user.router, prefix="/api/users", tags=["用户管理"])
app.include_router(order.router, prefix="/api/orders", tags=["订单管理"])
app.include_router(invoice.router, prefix="/api/invoices", tags=["发票管理"])

# 根路径
@app.get("/")
def read_root():
    return {"message": "欢迎使用订单管理系统"}