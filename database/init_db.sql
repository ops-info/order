-- 创建数据库
CREATE DATABASE IF NOT EXISTS order_management DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci;
USE order_management;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    password_hash VARCHAR(100) NOT NULL COMMENT '加密后的密码',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    phone VARCHAR(20) UNIQUE COMMENT '手机号',
    is_active TINYINT(1) DEFAULT 1 COMMENT '账号是否启用',
    is_first_login TINYINT(1) DEFAULT 1 COMMENT '是否首次登录',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表';

-- 创建订单表
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单ID',
    shop_id VARCHAR(50) NOT NULL COMMENT '店铺ID',
    order_number VARCHAR(50) NOT NULL UNIQUE COMMENT '订单号',
    price DECIMAL(10, 2) NOT NULL COMMENT '价格',
    status ENUM('买家已付款等待发货', '交易关闭', '交易成功', '部分退款', '卖家已发货等待买家确认') NOT NULL COMMENT '订单状态',
    audit_status ENUM('未审核', '已审核', '已结算', '未结算') DEFAULT '未审核' COMMENT '审核状态',
    remark VARCHAR(255) COMMENT '备注',
    settlement_time DATETIME COMMENT '结算时间',
    payment_time DATETIME COMMENT '付款时间',
    shipping_time DATETIME COMMENT '发货时间',
    closing_time DATETIME COMMENT '关闭时间',
    confirmation_time DATETIME COMMENT '确认收货时间',
    is_bound TINYINT(1) DEFAULT 1 COMMENT '订单绑定状态',
    user_id INT COMMENT '接单人ID',
    order_type ENUM('淘宝网') DEFAULT '淘宝网' COMMENT '订单类型',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_shop_id (shop_id),
    INDEX idx_order_number (order_number),
    INDEX idx_status (status),
    INDEX idx_audit_status (audit_status),
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单表';

-- 创建发票表
CREATE TABLE IF NOT EXISTS invoices (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '发票ID',
    invoice_number VARCHAR(50) NOT NULL UNIQUE COMMENT '发票号',
    order_id INT NOT NULL COMMENT '关联订单ID',
    amount DECIMAL(10, 2) NOT NULL COMMENT '金额',
    invoice_type VARCHAR(50) NOT NULL COMMENT '发票类型',
    issuing_date DATETIME NOT NULL COMMENT '开票日期',
    remark VARCHAR(255) COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_invoice_number (invoice_number),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='发票表';

-- 添加示例数据
-- 添加管理员用户
INSERT INTO users (username, password_hash, email, is_active, is_first_login)
VALUES (
    'admin', 
    '$2b$12$mKp5m1gH5T8yW8Zp2pK4eO9cJj8s7vLJZp4aYcJZp4qJZp4aYcJZ',  -- 密码: admin123
    'admin@example.com', 
    1, 
    1
);

-- 添加示例订单
INSERT INTO orders (shop_id, order_number, price, status, user_id)
VALUES 
('taobao_shop_1', 'TB123456789', 100.00, '买家已付款等待发货', 1),
('taobao_shop_2', 'TB987654321', 200.00, '交易成功', 1),
('taobao_shop_3', 'TB567891234', 150.00, '卖家已发货等待买家确认', NULL);

-- 添加示例发票
INSERT INTO invoices (invoice_number, order_id, amount, invoice_type, issuing_date)
VALUES 
('FP123456', 1, 100.00, '增值税专用发票', '2023-01-01'),
('FP654321', 2, 200.00, '增值税普通发票', '2023-01-02');