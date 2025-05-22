#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
医生实体类
"""

from typing import List

class Doctor:
    """<<Entity>> 医生实体类"""
    
    def __init__(self, id=None, full_name=None, email=None, assigned_clinics=None, specialisation=None):
        """初始化医生实体
        
        Args:
            id (int, optional): 医生ID
            full_name (str, optional): 全名
            email (str, optional): 电子邮箱
            assigned_clinics (list, optional): 所属诊所ID列表
            specialisation (list, optional): 专业领域列表
        """
        self.__id = int(id) if id is not None else None
        self.__full_name = str(full_name) if full_name is not None else None
        self.__email = str(email) if email is not None else None
        self.__assigned_clinics = assigned_clinics if assigned_clinics else []
        self.__specialisation = specialisation if specialisation else []
    
    # 访问器方法
    @property
    def id(self) -> int:
        """获取医生ID
        
        Returns:
            int: 医生ID
        """
        return self.__id
    
    @property
    def full_name(self) -> str:
        """获取医生全名
        
        Returns:
            str: 医生全名
        """
        return self.__full_name
    
    @property
    def email(self) -> str:
        """获取医生电子邮箱
        
        Returns:
            str: 医生电子邮箱
        """
        return self.__email
    
    @property
    def assigned_clinics(self) -> List[int]:
        """获取医生所属诊所ID列表
        
        Returns:
            List[int]: 医生所属诊所ID列表
        """
        return self.__assigned_clinics
    
    @property
    def specialisation(self) -> List[str]:
        """获取医生专业领域列表
        
        Returns:
            List[str]: 医生专业领域列表
        """
        return self.__specialisation
    
    # 修改器方法
    @full_name.setter
    def full_name(self, full_name: str) -> None:
        """设置医生全名
        
        Args:
            full_name (str): 医生全名
        """
        self.__full_name = str(full_name) if full_name is not None else None
    
    @email.setter
    def email(self, email: str) -> None:
        """设置医生电子邮箱
        
        Args:
            email (str): 医生电子邮箱
        """
        self.__email = str(email) if email is not None else None
    
    @assigned_clinics.setter
    def assigned_clinics(self, assigned_clinics: List[int]) -> None:
        """设置医生所属诊所ID列表
        
        Args:
            assigned_clinics (List[int]): 医生所属诊所ID列表
        """
        self.__assigned_clinics = assigned_clinics if assigned_clinics else []
    
    @specialisation.setter
    def specialisation(self, specialisation: List[str]) -> None:
        """设置医生专业领域列表
        
        Args:
            specialisation (List[str]): 医生专业领域列表
        """
        self.__specialisation = specialisation if specialisation else []
    
    # 业务方法
    def add_clinic(self, clinic_id: int) -> None:
        """添加医生所属诊所
        
        Args:
            clinic_id (int): 诊所ID
        """
        if clinic_id not in self.__assigned_clinics:
            self.__assigned_clinics.append(clinic_id)
    
    def remove_clinic(self, clinic_id: int) -> None:
        """移除医生所属诊所
        
        Args:
            clinic_id (int): 诊所ID
        """
        if clinic_id in self.__assigned_clinics:
            self.__assigned_clinics.remove(clinic_id)
    
    def add_specialisation(self, specialisation: str) -> None:
        """添加医生专业领域
        
        Args:
            specialisation (str): 专业领域
        """
        if specialisation not in self.__specialisation:
            self.__specialisation.append(specialisation)
    
    def remove_specialisation(self, specialisation: str) -> None:
        """移除医生专业领域
        
        Args:
            specialisation (str): 专业领域
        """
        if specialisation in self.__specialisation:
            self.__specialisation.remove(specialisation)
    
    def is_working_in_clinic(self, clinic_id: int) -> bool:
        """判断医生是否在指定诊所工作
        
        Args:
            clinic_id (int): 诊所ID
            
        Returns:
            bool: 如果医生在指定诊所工作返回True，否则返回False
        """
        return clinic_id in self.__assigned_clinics
    
    def has_specialisation(self, specialisation: str) -> bool:
        """判断医生是否具有指定专业领域
        
        Args:
            specialisation (str): 专业领域
            
        Returns:
            bool: 如果医生具有指定专业领域返回True，否则返回False
        """
        return specialisation in self.__specialisation
    
    def __str__(self) -> str:
        """返回医生字符串表示
        
        Returns:
            str: 医生字符串表示
        """
        return f"Doctor(id={self.__id}, full_name={self.__full_name}, clinics={self.__assigned_clinics})"
    
    def to_dict(self) -> dict:
        """转换为字典
        
        Returns:
            dict: 医生字典表示
        """
        return {
            "id": self.__id,
            "full_name": self.__full_name,
            "email": self.__email,
            "assigned_clinics": self.__assigned_clinics,
            "specialisation": self.__specialisation
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建医生
        
        Args:
            data (dict): 医生字典数据
            
        Returns:
            Doctor: 医生实体
        """
        # 处理assigned_clinics字段，可能是字符串形式的"1;2;3"
        assigned_clinics = data.get("assigned_clinics")
        if isinstance(assigned_clinics, str):
            assigned_clinics = [int(clinic_id) for clinic_id in assigned_clinics.split(";") if clinic_id]
        
        # 处理specialisation字段，可能是字符串形式的"专业1;专业2"
        specialisation = data.get("specialisation")
        if isinstance(specialisation, str):
            specialisation = [spec.strip() for spec in specialisation.split(";") if spec]
        
        return cls(
            id=data.get("id"),
            full_name=data.get("full_name"),
            email=data.get("email"),
            assigned_clinics=assigned_clinics,
            specialisation=specialisation
        ) 
