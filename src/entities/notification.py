#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Notification Entity Class
"""

class Notification:
    """<<Entity>> Notification Entity Class"""
    
    def __init__(self, id=None, user_id=None, message=None, date=None, read=False):
        """Initialize notification entity
        
        Args:
            id (int, optional): Notification ID
            user_id (int, optional): User ID
            message (str, optional): Notification message content
            date (str, optional): Date, format "YYYY-MM-DD"
            read (bool, optional): Whether the notification has been read
        """
        self.__id = int(id) if id is not None else None
        self.__user_id = int(user_id) if user_id is not None else None
        self.__message = str(message) if message is not None else None
        self.__date = str(date) if date is not None else None
        self.__read = read if isinstance(read, bool) else (str(read).lower() == "true")
    
    # Accessor methods
    @property
    def id(self) -> int:
        """Get notification ID
        
        Returns:
            int: Notification ID
        """
        return self.__id
    
    @property
    def user_id(self) -> int:
        """Get user ID
        
        Returns:
            int: User ID
        """
        return self.__user_id
    
    @property
    def message(self) -> str:
        """Get notification message content
        
        Returns:
            str: Notification message content
        """
        return self.__message
    
    @property
    def date(self) -> str:
        """Get date
        
        Returns:
            str: Date
        """
        return self.__date
    
    @property
    def read(self) -> bool:
        """Get read status
        
        Returns:
            bool: Whether the notification has been read
        """
        return self.__read
    
    # Modifier methods
    @user_id.setter
    def user_id(self, user_id: int) -> None:
        """Set user ID
        
        Args:
            user_id (int): User ID
        """
        self.__user_id = int(user_id) if user_id is not None else None
    
    @message.setter
    def message(self, message: str) -> None:
        """Set notification message content
        
        Args:
            message (str): Notification message content
        """
        self.__message = str(message) if message is not None else None
    
    @date.setter
    def date(self, date: str) -> None:
        """Set date
        
        Args:
            date (str): Date
        """
        self.__date = str(date) if date is not None else None
    
    @read.setter
    def read(self, read: bool) -> None:
        """Set read status
        
        Args:
            read (bool): Whether the notification has been read
        """
        self.__read = read if isinstance(read, bool) else (str(read).lower() == "true")
    
    # Business methods
    def mark_as_read(self) -> None:
        """Mark notification as read"""
        self.__read = True
    
    def mark_as_unread(self) -> None:
        """Mark notification as unread"""
        self.__read = False
    
    def __str__(self) -> str:
        """Return string representation of notification
        
        Returns:
            str: String representation of notification
        """
        return f"Notification(id={self.__id}, user_id={self.__user_id}, date={self.__date}, read={self.__read})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary
        
        Returns:
            dict: Dictionary representation of notification
        """
        return {
            "id": self.__id,
            "user_id": self.__user_id,
            "message": self.__message,
            "date": self.__date,
            "read": self.__read
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create notification from dictionary
        
        Args:
            data (dict): Dictionary data of notification
            
        Returns:
            Notification: Notification entity
        """
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            message=data.get("message"),
            date=data.get("date"),
            read=data.get("read")
        ) 