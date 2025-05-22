#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通知仓库类
"""

import os
from typing import List, Optional
from datetime import datetime
from src.entities.notification import Notification
from src.repositories.base_repository import BaseRepository

class NotificationRepository(BaseRepository[Notification]):
    """通知仓库类"""
    
    def __init__(self):
        """初始化通知仓库"""
        data_file = os.path.join("data", "notifications.csv")
        super().__init__(data_file, Notification)
    
    def get_by_user(self, user_id: int) -> List[Notification]:
        """根据用户ID获取通知列表
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            List[Notification]: 通知列表
        """
        notifications = self.get_all()
        return [notification for notification in notifications if notification.user_id == user_id]
    
    def get_unread_by_user(self, user_id: int) -> List[Notification]:
        """根据用户ID获取未读通知列表
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            List[Notification]: 未读通知列表
        """
        notifications = self.get_by_user(user_id)
        return [notification for notification in notifications if not notification.read]
    
    def mark_as_read(self, notification_id: int) -> bool:
        """将通知标记为已读
        
        Args:
            notification_id (int): 通知ID
            
        Returns:
            bool: 如果标记成功返回True，否则返回False
        """
        notification = self.get_by_id(notification_id)
        
        if not notification:
            return False
        
        notification.mark_as_read()
        self.update(notification)
        
        return True
    
    def mark_all_as_read(self, user_id: int) -> int:
        """将用户的所有通知标记为已读
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            int: 标记为已读的通知数量
        """
        unread_notifications = self.get_unread_by_user(user_id)
        count = 0
        
        for notification in unread_notifications:
            notification.mark_as_read()
            self.update(notification)
            count += 1
        
        return count
    
    def create_notification(self, user_id: int, message: str) -> Notification:
        """创建新通知
        
        Args:
            user_id (int): 用户ID
            message (str): 通知消息内容
            
        Returns:
            Notification: 创建的通知
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        notification = Notification(
            user_id=user_id,
            message=message,
            date=today,
            read=False
        )
        
        return self.add(notification) 