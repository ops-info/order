# 订单管理系统

这是一个用于对接淘宝网订单的管理系统，采用FastAPI + Vue + MySQL技术栈，支持用户管理、订单管理、发票管理等核心功能。

## 技术栈

### 后端
- **FastAPI**：高性能Web框架，提供API接口
- **SQLAlchemy**：ORM工具，用于数据库操作
- **MySQL 8.0**：关系型数据库，存储订单和用户数据
- **Docker**：容器化部署
- **Docker Compose**：服务编排

### 前端
- **Vue.js**：渐进式JavaScript框架
- **Element UI**：UI组件库
- **axios**：HTTP客户端
- **Vue Router**：路由管理

## 功能特性

### 用户模块
- 用户登录（支持验证码）
- 新用户创建（后台管理）
- 密码修改
- 首次登录提示修改密码

### 订单管理模块
- 订单列表展示（支持字段设置）
- 订单录入
- 订单搜索（多条件筛选）
- 订单发货操作
- 订单状态管理

### 发票模块
- 发票展示
- 发票信息录入

## 项目结构
```shell
order-management-system/
├── app/
│   ├── __init__.py
│   ├── main.py           # 入口文件
│   ├── models/           # 数据库模型
│   ├── schemas/          # Pydantic模型
│   ├── crud/             # 数据库操作
│   ├── routers/          # 路由
│   ├── utils/            # 工具类
│   ├── services/         # 业务服务
│   └── database.py       # 数据库配置
├── database/             # 数据库初始化脚本
├── frontend/             # Vue前端代码
├── .gitignore            # Git忽略文件
├── requirements.txt      # Python依赖
├── Dockerfile.backend    # 后端Dockerfile
├── frontend/Dockerfile   # 前端Dockerfile
├── docker-compose.yml    # Docker Compose配置
└── README.md             # 项目说明
```
## 安装与启动

### 前提条件
- Docker
- Docker Compose

### 构建与启动服务# 克隆项目
git clone https://github.com/your-repo/order-management-system.git
cd order-management-system

# 构建并启动服务
docker-compose up -d --build
### 访问应用
- 后端API: http://localhost:8000
- 前端界面: http://localhost:8080

### 初始账号
- 用户名: admin
- 密码: admin123

## API文档

启动服务后，可以访问以下URL查看API文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 数据模型

系统包含三个主要实体：
- 用户(User)
- 订单(Order)
- 发票(Invoice)

详细的数据模型定义见`app/models`目录和数据库初始化脚本。

## 贡献

欢迎贡献代码，请遵循以下步骤：
1. Fork项目
2. 创建新分支
3. 提交修改
4. 创建Pull Request

## 许可证

本项目采用MIT许可证，详情见LICENSE文件。