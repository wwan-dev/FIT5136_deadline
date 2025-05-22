#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
预约实体类
"""

class Appointment:
    """<<Entity>> 预约实体类"""
    
    def __init__(self, id=None, patient_email=None, doctor_id=None, clinic_id=None, 
                 date=None, time_slot=None, reason=None, status=None):
        """初始化预约实体
        
        Args:
            id (int, optional): 预约ID
            patient_email (str, optional): 患者电子邮箱
            doctor_id (int, optional): 医生ID
            clinic_id (int, optional): 诊所ID
            date (str, optional): 日期，格式为 "YYYY-MM-DD"
            time_slot (int, optional): 时间槽索引（0-15）
            reason (str, optional): 预约原因
            status (str, optional): 预约状态
        """
        self.__id = int(id) if id is not None else None
        self.__patient_email = str(patient_email) if patient_email is not None else None
        self.__doctor_id = int(doctor_id) if doctor_id is not None else None
        self.__clinic_id = int(clinic_id) if clinic_id is not None else None
        self.__date = str(date) if date is not None else None
        self.__time_slot = int(time_slot) if time_slot is not None else None
        self.__reason = str(reason) if reason is not None else None
        self.__status = str(status) if status is not None else None
    
    # 访问器方法
    @property
    def id(self) -> int:
        """获取预约ID
        
        Returns:
            int: 预约ID
        """
        return self.__id
    
    @property
    def patient_email(self) -> str:
        """获取患者电子邮箱
        
        Returns:
            str: 患者电子邮箱
        """
        return self.__patient_email
    
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
    def date(self) -> str:
        """获取日期
        
        Returns:
            str: 日期
        """
        return self.__date
    
    @property
    def time_slot(self) -> int:
        """获取时间槽索引
        
        Returns:
            int: 时间槽索引
        """
        return self.__time_slot
    
    @property
    def reason(self) -> str:
        """获取预约原因
        
        Returns:
            str: 预约原因
        """
        return self.__reason
    
    @property
    def status(self) -> str:
        """获取预约状态
        
        Returns:
            str: 预约状态
        """
        return self.__status
    
    # 修改器方法
    @patient_email.setter
    def patient_email(self, patient_email: str) -> None:
        """设置患者电子邮箱
        
        Args:
            patient_email (str): 患者电子邮箱
        """
        self.__patient_email = str(patient_email) if patient_email is not None else None
    
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
    
    @date.setter
    def date(self, date: str) -> None:
        """设置日期
        
        Args:
            date (str): 日期
        """
        self.__date = str(date) if date is not None else None
    
    @time_slot.setter
    def time_slot(self, time_slot: int) -> None:
        """设置时间槽索引
        
        Args:
            time_slot (int): 时间槽索引
        """
        self.__time_slot = int(time_slot) if time_slot is not None else None
    
    @reason.setter
    def reason(self, reason: str) -> None:
        """设置预约原因
        
        Args:
            reason (str): 预约原因
        """
        self.__reason = str(reason) if reason is not None else None
    
    @status.setter
    def status(self, status: str) -> None:
        """设置预约状态
        
        Args:
            status (str): 预约状态
        """
        self.__status = str(status) if status is not None else None
    
    # 业务方法
    def is_scheduled(self) -> bool:
        """判断预约是否已安排
        
        Returns:
            bool: 如果预约已安排返回True，否则返回False
        """
        return self.__status == "Scheduled"
    
    def is_completed(self) -> bool:
        """判断预约是否已完成
        
        Returns:
            bool: 如果预约已完成返回True，否则返回False
        """
        return self.__status == "Completed"
    
    def is_cancelled(self) -> bool:
        """判断预约是否已取消
        
        Returns:
            bool: 如果预约已取消返回True，否则返回False
        """
        return self.__status == "Cancelled by Patient" or self.__status == "Cancelled by Clinic"
    
    def mark_as_scheduled(self) -> None:
        """将预约标记为已安排"""
        self.__status = "Scheduled"
    
    def mark_as_completed(self) -> None:
        """将预约标记为已完成"""
        self.__status = "Completed"
    
    def cancel_by_patient(self) -> None:
        """患者取消预约"""
        self.__status = "Cancelled by Patient"
    
    def cancel_by_clinic(self) -> None:
        """诊所取消预约"""
        self.__status = "Cancelled by Clinic"
    
    def __str__(self) -> str:
        """返回预约字符串表示
        
        Returns:
            str: 预约字符串表示
        """
        return f"Appointment(id={self.__id}, patient={self.__patient_email}, doctor={self.__doctor_id}, date={self.__date}, time_slot={self.__time_slot}, status={self.__status})"
    
    def to_dict(self) -> dict:
        """转换为字典
        
        Returns:
            dict: 预约字典表示
        """
        return {
            "id": self.__id,
            "patient_email": self.__patient_email,
            "doctor_id": self.__doctor_id,
            "clinic_id": self.__clinic_id,
            "date": self.__date,
            "time_slot": self.__time_slot,
            "reason": self.__reason,
            "status": self.__status
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建预约
        
        Args:
            data (dict): 预约字典数据
            
        Returns:
            Appointment: 预约实体
        """
        return cls(
            id=data.get("id"),
            patient_email=data.get("patient_email"),
            doctor_id=data.get("doctor_id"),
            clinic_id=data.get("clinic_id"),
            date=data.get("date"),
            time_slot=data.get("time_slot"),
            reason=data.get("reason"),
            status=data.get("status")
        ) 
