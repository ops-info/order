from sqlalchemy.orm import Session
from models import order as order_models
from schemas import order as order_schemas
from crud import order as order_crud
from utils.taobao_client import TaobaoClient
from datetime import datetime, timedelta
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderSyncService:
    """订单同步服务"""
    
    def __init__(self, db: Session, taobao_client: TaobaoClient):
        """
        初始化订单同步服务
        
        Args:
            db: 数据库会话
            taobao_client: 淘宝API客户端
        """
        self.db = db
        self.taobao_client = taobao_client
    
    def sync_orders(self, session: str, days: int = 7) -> int:
        """
        从淘宝同步订单
        
        Args:
            session: 淘宝会话令牌
            days: 同步最近多少天的订单
            
        Returns:
            同步的订单数量
        """
        # 计算开始和结束时间
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
        
        logger.info(f"开始同步淘宝订单，时间范围: {start_time_str} - {end_time_str}")
        
        page_no = 1
        page_size = 100
        total_synced = 0
        has_next = True
        
        while has_next:
            # 获取淘宝订单
            try:
                response = self.taobao_client.get_orders(
                    session=session,
                    start_time=start_time_str,
                    end_time=end_time_str,
                    page_no=page_no,
                    page_size=page_size
                )
            except Exception as e:
                logger.error(f"获取淘宝订单失败: {str(e)}")
                break
            
            # 检查响应
            if "trades_sold_get_response" not in response:
                logger.error(f"获取淘宝订单失败，响应格式错误: {response}")
                break
            
            response_data = response["trades_sold_get_response"]
            
            if "trades" not in response_data or "trade" not in response_data["trades"]:
                logger.info(f"没有更多订单需要同步")
                break
            
            trades = response_data["trades"]["trade"]
            
            # 处理每个订单
            for trade in trades:
                try:
                    self._process_taobao_order(trade)
                    total_synced += 1
                except Exception as e:
                    logger.error(f"处理订单 {trade.get('tid')} 失败: {str(e)}")
            
            # 检查是否有下一页
            has_next = response_data.get("has_next", False)
            page_no += 1
            
            logger.info(f"已同步 {total_synced} 个订单，当前页: {page_no-1}, 还有下一页: {has_next}")
        
        logger.info(f"订单同步完成，共同步 {total_synced} 个订单")
        return total_synced
    
    def _process_taobao_order(self, trade: dict) -> None:
        """
        处理单个淘宝订单
        
        Args:
            trade: 淘宝订单数据
        """
        # 检查订单是否已存在
        tid = trade.get("tid")
        if not tid:
            raise ValueError("订单缺少必要字段: tid")
        
        db_order = order_crud.get_order_by_number(self.db, order_number=str(tid))
        
        # 转换订单状态
        status_map = {
            "WAIT_SELLER_SEND_GOODS": order_schemas.OrderStatus.WAITING_FOR_SHIPMENT,
            "TRADE_CLOSED": order_schemas.OrderStatus.CLOSED,
            "TRADE_FINISHED": order_schemas.OrderStatus.SUCCESS,
            "TRADE_CLOSED_BY_TAOBAO": order_schemas.OrderStatus.CLOSED,
            "WAIT_BUYER_CONFIRM_GOODS": order_schemas.OrderStatus.SHIPPED
        }
        
        taobao_status = trade.get("status")
        status = status_map.get(taobao_status, taobao_status)
        
        # 转换支付时间
        pay_time = trade.get("pay_time")
        if pay_time:
            pay_time = datetime.strptime(pay_time, "%Y-%m-%d %H:%M:%S")
        
        # 转换订单数据
        order_data = {
            "shop_id": trade.get("seller_nick", ""),
            "order_number": str(tid),
            "price": float(trade.get("payment", 0)),
            "status": status,
            "payment_time": pay_time,
            "remark": trade.get("buyer_message", "")
        }
        
        if db_order:
            # 更新现有订单
            order_update = order_schemas.OrderUpdate(**order_data)
            order_crud.update_order(self.db, db_order.id, order_update)
        else:
            # 创建新订单
            order_create = order_schemas.OrderCreate(**order_data)
            order_crud.create_order(self.db, order_create)