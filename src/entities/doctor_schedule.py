#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
医生排班实体类
"""

class DoctorSchedule:
    """<<Entity>> 医生排班实体类"""
    
    def __init__(self, id=None, doctor_id=None, clinic_id=None, time_slots=None):
        """初始化医生排班实体
        
        Args:
            id (int, optional): 排班ID
            doctor_id (int, optional): 医生ID
            clinic_id (int, optional): 诊所ID
            time_slots (str, optional): 16进制表示的时间槽
        """
        self.__id = int(id) if id is not None else None
        self.__doctor_id = int(doctor_id) if doctor_id is not None else None
        self.__clinic_id = int(clinic_id) if clinic_id is not None else None
        self.__time_slots = str(time_slots) if time_slots is not None else None
    
    # 访问器方法
    @property
    def id(self) -> int:
        """获取排班ID
        
        Returns:
            int: 排班ID
        """
        return self.__id
    
    @property
    def doctor_id(self) -> int:
        """获取医生ID
        
        Returns:
            int: 医生ID
        """
        return self.__doctor_id
    
    @property
    def clinic_id(self) -> int:
        """获取诊所ID
        
        Returns:
            int: 诊所ID
        """
        return self.__clinic_id
    
    @property
    def time_slots(self) -> str:
        """获取时间槽
        
        Returns:
            str: 16进制表示的时间槽
        """
        return self.__time_slots
    
    # 修改器方法
    @doctor_id.setter
    def doctor_id(self, doctor_id: int) -> None:
        """设置医生ID
        
        Args:
            doctor_id (int): 医生ID
        """
        self.__doctor_id = int(doctor_id) if doctor_id is not None else None
    
    @clinic_id.setter
    def clinic_id(self, clinic_id: int) -> None:
        """设置诊所ID
        
        Args:
            clinic_id (int): 诊所ID
        """
        self.__clinic_id = int(clinic_id) if clinic_id is not None else None
    
    @time_slots.setter
    def time_slots(self, time_slots: str) -> None:
        """设置时间槽
        
        Args:
            time_slots (str): 16进制表示的时间槽
        """
        self.__time_slots = str(time_slots) if time_slots is not None else None
    
    # 业务方法
    def is_available(self, time_slot_index: int) -> bool:
        """判断指定时间槽是否可用
        
        Args:
            time_slot_index (int): 时间槽索引（0-15）
            
        Returns:
            bool: 如果时间槽可用返回True，否则返回False
        """
        if not self.__time_slots:
            return False
        
        # 将16进制字符串转换为整数
        time_slots_int = int(self.__time_slots, 16)
        
        # 检查对应位置的位是否为1（可用）
        return (time_slots_int & (1 << time_slot_index)) != 0
    
    def set_available(self, time_slot_index: int) -> None:
        """设置指定时间槽为可用
        
        Args:
            time_slot_index (int): 时间槽索引（0-15）
        """
        if not self.__time_slots:
            self.__time_slots = "0"
        
        # 将16进制字符串转换为整数
        time_slots_int = int(self.__time_slots, 16)
        
        # 设置对应位置的位为1（可用）
        time_slots_int |= (1 << time_slot_index)
        
        # 转换回16进制字符串
        self.__time_slots = format(time_slots_int, 'x')
    
    def set_unavailable(self, time_slot_index: int) -> None:
        """设置指定时间槽为不可用
        
        Args:
            time_slot_index (int): 时间槽索引（0-15）
        """
        if not self.__time_slots:
            return
        
        # 将16进制字符串转换为整数
        time_slots_int = int(self.__time_slots, 16)
        
        # 设置对应位置的位为0（不可用）
        time_slots_int &= ~(1 << time_slot_index)
        
        # 转换回16进制字符串
        self.__time_slots = format(time_slots_int, 'x')
    
    def __str__(self) -> str:
        """返回医生排班字符串表示
        
        Returns:
            str: 医生排班字符串表示
        """
        return f"DoctorSchedule(id={self.__id}, doctor_id={self.__doctor_id}, clinic_id={self.__clinic_id}, time_slots={self.__time_slots})"
    
    def to_dict(self) -> dict:
        """转换为字典
        
        Returns:
            dict: 医生排班字典表示
        """
        return {
            "id": self.__id,
            "doctor_id": self.__doctor_id,
            "clinic_id": self.__clinic_id,
            "time_slots": self.__time_slots
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建医生排班
        
        Args:
            data (dict): 医生排班字典数据
            
        Returns:
            DoctorSchedule: 医生排班实体
        """
        return cls(
            id=data.get("id"),
            doctor_id=data.get("doctor_id"),
            clinic_id=data.get("clinic_id"),
            time_slots=data.get("time_slots")
        ) 