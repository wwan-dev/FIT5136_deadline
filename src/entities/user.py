#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户实体类
"""

class User:
    """<<Entity>> 用户实体类"""
    
    def __init__(self, user_id=None, email=None, password=None, role=None, name=None, phone=None, address=None,
                 date_of_birth=None, gender=None, medical_history=None):
        """初始化用户实体
        
        Args:
            user_id (int, optional): 用户ID
            email (str, optional): 电子邮箱
            password (str, optional): 密码
            role (str, optional): 角色（patient/admin）
            name (str, optional): 姓名
            phone (str, optional): 电话号码
            address (str, optional): 地址
            date_of_birth (str, optional): 出生日期，格式为 "YYYY-MM-DD"，仅患者需要
            gender (str, optional): 性别，仅患者需要
            medical_history (str, optional): 病史，仅患者需要
        """
        self.__id = int(user_id) if user_id is not None else None
        self.__email = str(email) if email is not None else None
        self.__password = str(password) if password is not None else None
        self.__role = str(role) if role is not None else None
        self.__name = str(name) if name is not None else None
        self.__phone = str(phone) if phone is not None else None
        self.__address = str(address) if address is not None else None
        self.__date_of_birth = str(date_of_birth) if date_of_birth is not None else None
        self.__gender = str(gender) if gender is not None else None
        self.__medical_history = str(medical_history) if medical_history is not None else None
    
    # 访问器方法
    @property
    def id(self) -> int:
        """获取用户ID
        
        Returns:
            int: 用户ID
        """
        return self.__id
    
    @property
    def email(self) -> str:
        """获取用户电子邮箱
        
        Returns:
            str: 用户电子邮箱
        """
        return self.__email
    
    @property
    def password(self) -> str:
        """获取用户密码
        
        Returns:
            str: 用户密码
        """
        return self.__password
    
    @property
    def role(self) -> str:
        """获取用户角色
        
        Returns:
            str: 用户角色
        """
        return self.__role
    
    @property
    def name(self) -> str:
        """获取用户姓名
        
        Returns:
            str: 用户姓名
        """
        return self.__name
    
    @property
    def phone(self) -> str:
        """获取用户电话号码
        
        Returns:
            str: 用户电话号码
        """
        return self.__phone
    
    @property
    def address(self) -> str:
        """获取用户地址
        
        Returns:
            str: 用户地址
        """
        return self.__address
    
    @property
    def date_of_birth(self) -> str:
        """获取用户出生日期
        
        Returns:
            str: 用户出生日期
        """
        return self.__date_of_birth
    
    @property
    def gender(self) -> str:
        """获取用户性别
        
        Returns:
            str: 用户性别
        """
        return self.__gender
    
    @property
    def medical_history(self) -> str:
        """获取用户病史
        
        Returns:
            str: 用户病史
        """
        return self.__medical_history
    
    # 修改器方法
    @email.setter
    def email(self, email: str) -> None:
        """设置用户电子邮箱
        
        Args:
            email (str): 用户电子邮箱
        """
        self.__email = str(email) if email is not None else None
    
    @password.setter
    def password(self, password: str) -> None:
        """设置用户密码
        
        Args:
            password (str): 用户密码
        """
        self.__password = str(password) if password is not None else None
    
    @role.setter
    def role(self, role: str) -> None:
        """设置用户角色
        
        Args:
            role (str): 用户角色
        """
        self.__role = str(role) if role is not None else None
    
    @name.setter
    def name(self, name: str) -> None:
        """设置用户姓名
        
        Args:
            name (str): 用户姓名
        """
        self.__name = str(name) if name is not None else None
    
    @phone.setter
    def phone(self, phone: str) -> None:
        """设置用户电话号码
        
        Args:
            phone (str): 用户电话号码
        """
        self.__phone = str(phone) if phone is not None else None
    
    @address.setter
    def address(self, address: str) -> None:
        """设置用户地址
        
        Args:
            address (str): 用户地址
        """
        self.__address = str(address) if address is not None else None
    
    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: str) -> None:
        """设置用户出生日期
        
        Args:
            date_of_birth (str): 用户出生日期
        """
        self.__date_of_birth = str(date_of_birth) if date_of_birth is not None else None
    
    @gender.setter
    def gender(self, gender: str) -> None:
        """设置用户性别
        
        Args:
            gender (str): 用户性别
        """
        self.__gender = str(gender) if gender is not None else None
    
    @medical_history.setter
    def medical_history(self, medical_history: str) -> None:
        """设置用户病史
        
        Args:
            medical_history (str): 用户病史
        """
        self.__medical_history = str(medical_history) if medical_history is not None else None
    
    # 业务方法
    def is_admin(self) -> bool:
        """判断是否是管理员
        
        Returns:
            bool: 如果是管理员返回True，否则返回False
        """
        return self.__role == "admin"
    
    def is_patient(self) -> bool:
        """判断是否是患者
        
        Returns:
            bool: 如果是患者返回True，否则返回False
        """
        return self.__role == "patient"
    
    def __str__(self) -> str:
        """返回用户字符串表示
        
        Returns:
            str: 用户字符串表示
        """
        if self.is_patient():
            return f"User(id={self.__id}, email={self.__email}, role={self.__role}, name={self.__name}, gender={self.__gender})"
        else:
            return f"User(id={self.__id}, email={self.__email}, role={self.__role}, name={self.__name})"
    
    def to_dict(self) -> dict:
        """转换为字典
        
        Returns:
            dict: 用户字典表示
        """
        data = {
            "id": self.__id,
            "email": self.__email,
            "password": self.__password,
            "role": self.__role,
            "name": self.__name,
            "phone": self.__phone,
            "address": self.__address
        }
        
        # 仅当用户是患者时添加患者特有字段
        if self.is_patient():
            data.update({
                "date_of_birth": self.__date_of_birth,
                "gender": self.__gender,
                "medical_history": self.__medical_history
            })
            
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建用户
        
        Args:
            data (dict): 用户字典数据
            
        Returns:
            User: 用户实体
        """
        return cls(
            user_id=data.get("id"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
            name=data.get("name"),
            phone=data.get("phone"),
            address=data.get("address"),
            date_of_birth=data.get("date_of_birth"),
            gender=data.get("gender"),
            medical_history=data.get("medical_history")
        ) 
