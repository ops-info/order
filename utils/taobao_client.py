import requests
import json
import hmac
import hashlib
import time
from typing import Dict, Any, Optional
from urllib.parse import urlencode

class TaobaoClient:
    """淘宝API客户端"""
    
    def __init__(self, app_key: str, app_secret: str, sandbox: bool = False):
        """
        初始化淘宝API客户端
        
        Args:
            app_key: 应用Key
            app_secret: 应用密钥
            sandbox: 是否使用沙箱环境
        """
        self.app_key = app_key
        self.app_secret = app_secret
        self.sandbox = sandbox
        
        if sandbox:
            self.api_url = "https://gw.api.tbsandbox.com/router/rest"
        else:
            self.api_url = "https://eco.taobao.com/router/rest"
    
    def generate_sign(self, params: Dict[str, Any]) -> str:
        """
        生成API请求签名
        
        Args:
            params: 请求参数
            
        Returns:
            签名结果
        """
        # 排序参数
        sorted_params = sorted(params.items(), key=lambda x: x[0])
        
        # 拼接参数字符串
        sign_str = self.app_secret
        for key, value in sorted_params:
            sign_str += f"{key}{value}"
        sign_str += self.app_secret
        
        # 计算签名
        sign = hmac.new(
            self.app_secret.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.md5
        ).hexdigest().upper()
        
        return sign
    
    def execute(self, method: str, params: Dict[str, Any], session: Optional[str] = None) -> Dict[str, Any]:
        """
        执行API请求
        
        Args:
            method: API方法名
            params: 请求参数
            session: 会话令牌（可选）
            
        Returns:
            API响应结果
        """
        # 构建公共参数
        common_params = {
            "app_key": self.app_key,
            "method": method,
            "format": "json",
            "v": "2.0",
            "sign_method": "md5",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
        
        # 添加会话令牌（如果有）
        if session:
            common_params["session"] = session
        
        # 合并参数
        all_params = {**common_params, **params}
        
        # 生成签名
        sign = self.generate_sign(all_params)
        
        # 添加签名到参数
        all_params["sign"] = sign
        
        # 发送请求
        response = requests.post(
            self.api_url,
            data=all_params,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # 解析响应
        try:
            result = response.json()
            return result
        except json.JSONDecodeError:
            raise Exception(f"解析响应失败: {response.text}")
    
    def get_orders(self, session: str, start_time: str, end_time: str, page_no: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """
        获取淘宝订单列表
        
        Args:
            session: 会话令牌
            start_time: 开始时间（格式：YYYY-MM-DD HH:MM:SS）
            end_time: 结束时间（格式：YYYY-MM-DD HH:MM:SS）
            page_no: 页码
            page_size: 每页数量
            
        Returns:
            订单列表结果
        """
        method = "taobao.trades.sold.get"
        params = {
            "fields": "tid,title,type,status,payment,discount_fee,adjust_fee,post_fee,total_fee,"
                      "pay_time,end_time,created,seller_nick,buyer_nick,buyer_message,"
                      "receiver_name,receiver_state,receiver_city,receiver_district,"
                      "receiver_address,receiver_zip,receiver_mobile,receiver_phone",
            "start_created": start_time,
            "end_created": end_time,
            "page_no": page_no,
            "page_size": page_size,
            "use_has_next": True
        }
        
        return self.execute(method, params, session)
    
    def get_order_detail(self, session: str, tid: int) -> Dict[str, Any]:
        """
        获取淘宝订单详情
        
        Args:
            session: 会话令牌
            tid: 订单ID
            
        Returns:
            订单详情结果
        """
        method = "taobao.trade.fullinfo.get"
        params = {
            "fields": "tid,title,type,status,payment,discount_fee,adjust_fee,post_fee,total_fee,"
                      "pay_time,end_time,created,seller_nick,buyer_nick,buyer_message,"
                      "receiver_name,receiver_state,receiver_city,receiver_district,"
                      "receiver_address,receiver_zip,receiver_mobile,receiver_phone,"
                      "orders.item_meal_name,orders.title,orders.price,orders.num,orders.total_fee,"
                      "orders.payment,orders.discount_fee,orders.adjust_fee,orders.status,"
                      "orders.sku_properties_name,orders.refund_status,orders.outer_iid,orders.outer_sku_id,"
                      "orders.seller_type",
            "tid": tid
        }
        
        return self.execute(method, params, session)