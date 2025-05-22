#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
诊所实体类
"""

class Clinic:
    """<<Entity>> 诊所实体类"""
    
    def __init__(self, clinic_id=None, name=None, suburb=None, address=None, phone=None):
        """初始化诊所实体
        
        Args:
            clinic_id (int, optional): 诊所ID
            name (str, optional): 诊所名称
            suburb (str, optional): 所在郊区
            address (str, optional): 地址
            phone (str, optional): 电话号码
        """
        self.__id = int(clinic_id) if clinic_id is not None else None
        self.__name = str(name) if name is not None else None
        self.__suburb = str(suburb) if suburb is not None else None
        self.__address = str(address) if address is not None else None
        self.__phone = str(phone) if phone is not None else None
    
    # 访问器方法
    @property
    def id(self) -> int:
        """获取诊所ID
        
        Returns:
            int: 诊所ID
        """
        return self.__id
    
    @property
    def name(self) -> str:
        """获取诊所名称
        
        Returns:
            str: 诊所名称
        """
        return self.__name
    
    @property
    def suburb(self) -> str:
        """获取诊所所在郊区
        
        Returns:
            str: 诊所所在郊区
        """
        return self.__suburb
    
    @property
    def address(self) -> str:
        """获取诊所地址
        
        Returns:
            str: 诊所地址
        """
        return self.__address
    
    @property
    def phone(self) -> str:
        """获取诊所电话号码
        
        Returns:
            str: 诊所电话号码
        """
        return self.__phone
    
    # 修改器方法
    @name.setter
    def name(self, name: str) -> None:
        """设置诊所名称
        
        Args:
            name (str): 诊所名称
        """
        self.__name = str(name) if name is not None else None
    
    @suburb.setter
    def suburb(self, suburb: str) -> None:
        """设置诊所所在郊区
        
        Args:
            suburb (str): 诊所所在郊区
        """
        self.__suburb = str(suburb) if suburb is not None else None
    
    @address.setter
    def address(self, address: str) -> None:
        """设置诊所地址
        
        Args:
            address (str): 诊所地址
        """
        self.__address = str(address) if address is not None else None
    
    @phone.setter
    def phone(self, phone: str) -> None:
        """设置诊所电话号码
        
        Args:
            phone (str): 诊所电话号码
        """
        self.__phone = str(phone) if phone is not None else None
    
    def __str__(self) -> str:
        """返回诊所字符串表示
        
        Returns:
            str: 诊所字符串表示
        """
        return f"Clinic(id={self.__id}, name={self.__name}, suburb={self.__suburb})"
    
    def to_dict(self) -> dict:
        """转换为字典
        
        Returns:
            dict: 诊所字典表示
        """
        return {
            "id": self.__id,
            "name": self.__name,
            "suburb": self.__suburb,
            "address": self.__address,
            "phone": self.__phone
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建诊所
        
        Args:
            data (dict): 诊所字典数据
            
        Returns:
            Clinic: 诊所实体
        """
        return cls(
            clinic_id=data.get("id"),
            name=data.get("name"),
            suburb=data.get("suburb"),
            address=data.get("address"),
            phone=data.get("phone")
        ) 