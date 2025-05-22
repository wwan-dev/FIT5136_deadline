#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通知实体类
"""

class Notification:
    """<<Entity>> 通知实体类"""
    
    def __init__(self, id=None, user_id=None, message=None, date=None, read=False):
        """初始化通知实体
        
        Args:
            id (int, optional): 通知ID
            user_id (int, optional): 用户ID
            message (str, optional): 通知消息内容
            date (str, optional): 日期，格式为 "YYYY-MM-DD"
            read (bool, optional): 是否已读
        """
        self.__id = int(id) if id is not None else None
        self.__user_id = int(user_id) if user_id is not None else None
        self.__message = str(message) if message is not None else None
        self.__date = str(date) if date is not None else None
        self.__read = read if isinstance(read, bool) else (str(read).lower() == "true")
    
    # 访问器方法
    @property
    def id(self) -> int:
        """获取通知ID
        
        Returns:
            int: 通知ID
        """
        return self.__id
    
    @property
    def user_id(self) -> int:
        """获取用户ID
        
        Returns:
            int: 用户ID
        """
        return self.__user_id
    
    @property
    def message(self) -> str:
        """获取通知消息内容
        
        Returns:
            str: 通知消息内容
        """
        return self.__message
    
    @property
    def date(self) -> str:
        """获取日期
        
        Returns:
            str: 日期
        """
        return self.__date
    
    @property
    def read(self) -> bool:
        """获取是否已读
        
        Returns:
            bool: 是否已读
        """
        return self.__read
    
    # 修改器方法
    @user_id.setter
    def user_id(self, user_id: int) -> None:
        """设置用户ID
        
        Args:
            user_id (int): 用户ID
        """
        self.__user_id = int(user_id) if user_id is not None else None
    
    @message.setter
    def message(self, message: str) -> None:
        """设置通知消息内容
        
        Args:
            message (str): 通知消息内容
        """
        self.__message = str(message) if message is not None else None
    
    @date.setter
    def date(self, date: str) -> None:
        """设置日期
        
        Args:
            date (str): 日期
        """
        self.__date = str(date) if date is not None else None
    
    @read.setter
    def read(self, read: bool) -> None:
        """设置是否已读
        
        Args:
            read (bool): 是否已读
        """
        self.__read = read if isinstance(read, bool) else (str(read).lower() == "true")
    
    # 业务方法
    def mark_as_read(self) -> None:
        """将通知标记为已读"""
        self.__read = True
    
    def mark_as_unread(self) -> None:
        """将通知标记为未读"""
        self.__read = False
    
    def __str__(self) -> str:
        """返回通知字符串表示
        
        Returns:
            str: 通知字符串表示
        """
        return f"Notification(id={self.__id}, user_id={self.__user_id}, date={self.__date}, read={self.__read})"
    
    def to_dict(self) -> dict:
        """转换为字典
        
        Returns:
            dict: 通知字典表示
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
        """从字典创建通知
        
        Args:
            data (dict): 通知字典数据
            
        Returns:
            Notification: 通知实体
        """
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            message=data.get("message"),
            date=data.get("date"),
            read=data.get("read")
        ) 