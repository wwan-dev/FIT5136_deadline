#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通知服务类 - 处理通知相关业务逻辑
"""

from typing import List, Optional
from src.entities.notification import Notification
from src.repositories.notification_repository import NotificationRepository

class NotificationService:
    """通知服务类"""
    
    def __init__(self):
        """初始化通知服务"""
        self.__notification_repo = NotificationRepository()
    
    def get_notifications_by_user(self, user_id: int) -> List[Notification]:
        """获取用户的所有通知
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            List[Notification]: 通知列表
        """
        return self.__notification_repo.get_by_user(user_id)
    
    def get_unread_notifications(self, user_id: int) -> List[Notification]:
        """获取用户的未读通知
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            List[Notification]: 未读通知列表
        """
        return self.__notification_repo.get_unread_by_user(user_id)
    
    def mark_notification_as_read(self, notification_id: int) -> bool:
        """将单个通知标记为已读
        
        Args:
            notification_id (int): 通知ID
            
        Returns:
            bool: 如果标记成功返回True，否则返回False
        """
        return self.__notification_repo.mark_as_read(notification_id)
    
    def mark_all_notifications_as_read(self, user_id: int) -> int:
        """将用户的所有通知标记为已读
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            int: 标记为已读的通知数量
        """
        return self.__notification_repo.mark_all_as_read(user_id)
    
    def create_notification(self, user_id: int, message: str) -> Notification:
        """创建新通知
        
        Args:
            user_id (int): 用户ID
            message (str): 通知消息内容
            
        Returns:
            Notification: 创建的通知
        """
        return self.__notification_repo.create_notification(user_id, message)
    
    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """根据ID获取通知
        
        Args:
            notification_id (int): 通知ID
            
        Returns:
            Optional[Notification]: 通知对象，如果不存在则返回None
        """
        return self.__notification_repo.get_by_id(notification_id) 