#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Notification Repository Class
"""

import os
from typing import List, Optional
from datetime import datetime
from src.entities.notification import Notification
from src.repositories.base_repository import BaseRepository

class NotificationRepository(BaseRepository[Notification]):
    """Notification Repository Class"""
    
    def __init__(self):
        """Initialize notification repository"""
        data_file = os.path.join("data", "notifications.csv")
        super().__init__(data_file, Notification)
    
    def get_by_user(self, user_id: int) -> List[Notification]:
        """Get notifications by user ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            List[Notification]: List of notifications
        """
        notifications = self.get_all()
        return [notification for notification in notifications if notification.user_id == user_id]
    
    def get_unread_by_user(self, user_id: int) -> List[Notification]:
        """Get unread notifications by user ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            List[Notification]: List of unread notifications
        """
        notifications = self.get_by_user(user_id)
        return [notification for notification in notifications if not notification.read]
    
    def mark_as_read(self, notification_id: int) -> bool:
        """Mark notification as read
        
        Args:
            notification_id (int): Notification ID
            
        Returns:
            bool: True if marked successfully, False otherwise
        """
        notification = self.get_by_id(notification_id)
        
        if not notification:
            return False
        
        notification.mark_as_read()
        self.update(notification)
        
        return True
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications of a user as read
        
        Args:
            user_id (int): User ID
            
        Returns:
            int: Number of notifications marked as read
        """
        unread_notifications = self.get_unread_by_user(user_id)
        count = 0
        
        for notification in unread_notifications:
            notification.mark_as_read()
            self.update(notification)
            count += 1
        
        return count
    
    def create_notification(self, user_id: int, message: str) -> Notification:
        """Create a new notification
        
        Args:
            user_id (int): User ID
            message (str): Notification message
            
        Returns:
            Notification: Created notification
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        notification = Notification(
            user_id=user_id,
            message=message,
            date=today,
            read=False
        )
        
        return self.add(notification) 