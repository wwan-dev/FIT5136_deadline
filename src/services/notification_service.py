#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Notification Service Class - Handles notification related business logic
"""

from typing import List, Optional
from src.entities.notification import Notification
from src.repositories.notification_repository import NotificationRepository

class NotificationService:
    """Notification Service Class"""
    
    def __init__(self):
        """Initialize notification service"""
        self.__notification_repo = NotificationRepository()
    
    def get_notifications_by_user(self, user_id: int) -> List[Notification]:
        """Get all notifications for a user
        
        Args:
            user_id (int): User ID
            
        Returns:
            List[Notification]: List of notifications
        """
        return self.__notification_repo.get_by_user(user_id)
    
    def get_unread_notifications(self, user_id: int) -> List[Notification]:
        """Get unread notifications for a user
        
        Args:
            user_id (int): User ID
            
        Returns:
            List[Notification]: List of unread notifications
        """
        return self.__notification_repo.get_unread_by_user(user_id)
    
    def mark_notification_as_read(self, notification_id: int) -> bool:
        """Mark a notification as read
        
        Args:
            notification_id (int): Notification ID
            
        Returns:
            bool: True if marked successfully, False otherwise
        """
        return self.__notification_repo.mark_as_read(notification_id)
    
    def mark_all_notifications_as_read(self, user_id: int) -> int:
        """Mark all notifications of a user as read
        
        Args:
            user_id (int): User ID
            
        Returns:
            int: Number of notifications marked as read
        """
        return self.__notification_repo.mark_all_as_read(user_id)
    
    def create_notification(self, user_id: int, message: str) -> Notification:
        """Create a new notification
        
        Args:
            user_id (int): User ID
            message (str): Notification message
            
        Returns:
            Notification: Created notification
        """
        return self.__notification_repo.create_notification(user_id, message)
    
    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """Get notification by ID
        
        Args:
            notification_id (int): Notification ID
            
        Returns:
            Optional[Notification]: Notification object, None if not found
        """
        return self.__notification_repo.get_by_id(notification_id) 