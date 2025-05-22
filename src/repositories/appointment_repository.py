#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
预约仓库类
"""

import os
from typing import List, Optional
from datetime import datetime
from src.entities.appointment import Appointment
from src.repositories.base_repository import BaseRepository
from src.repositories.doctor_schedule_repository import DoctorScheduleRepository

class AppointmentRepository(BaseRepository[Appointment]):
    """预约仓库类"""
    
    def __init__(self):
        """初始化预约仓库"""
        data_file = os.path.join("data", "appointments.csv")
        super().__init__(data_file, Appointment)
        self.__schedule_repo = DoctorScheduleRepository()
    
    def get_by_user(self, user_id: int) -> List[Appointment]:
        """根据用户ID获取预约列表
        
        Args:
            user_id (int): 用户ID
            
        Returns:
            List[Appointment]: 预约列表
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.user_id == user_id]
    
    # 兼容旧代码的方法
    def get_by_patient(self, patient_email: str) -> List[Appointment]:
        """根据患者电子邮箱获取预约列表（兼容旧代码）
        
        Args:
            patient_email (str): 患者电子邮箱或用户ID
            
        Returns:
            List[Appointment]: 预约列表
        """
        # 如果参数是数字，则认为是用户ID
        if isinstance(patient_email, int) or (isinstance(patient_email, str) and patient_email.isdigit()):
            user_id = int(patient_email)
            return self.get_by_user(user_id)
            
        # 否则，需要先从用户仓库查找对应的用户ID
        from src.repositories.user_repository import UserRepository
        user_repo = UserRepository()
        users = user_repo.get_all()
        
        for user in users:
            if user.email == patient_email:
                return self.get_by_user(user.id)
        
        # 如果找不到匹配的用户，返回空列表
        return []
    
    def get_by_doctor(self, doctor_id: int) -> List[Appointment]:
        """根据医生ID获取预约列表
        
        Args:
            doctor_id (int): 医生ID
            
        Returns:
            List[Appointment]: 预约列表
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.doctor_id == doctor_id]
    
    def get_by_clinic(self, clinic_id: int) -> List[Appointment]:
        """根据诊所ID获取预约列表
        
        Args:
            clinic_id (int): 诊所ID
            
        Returns:
            List[Appointment]: 预约列表
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.clinic_id == clinic_id]
    
    def get_by_date(self, date: str) -> List[Appointment]:
        """根据日期获取预约列表
        
        Args:
            date (str): 日期，格式为 "YYYY-MM-DD"
            
        Returns:
            List[Appointment]: 预约列表
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.date == date]
    
    def get_scheduled_appointments(self) -> List[Appointment]:
        """获取已安排的预约列表
        
        Returns:
            List[Appointment]: 预约列表
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.is_scheduled()]
    
    def get_completed_appointments(self) -> List[Appointment]:
        """获取已完成的预约列表
        
        Returns:
            List[Appointment]: 预约列表
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.is_completed()]
    
    def get_cancelled_appointments(self) -> List[Appointment]:
        """获取已取消的预约列表
        
        Returns:
            List[Appointment]: 预约列表
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.is_cancelled()]
    
    def get_future_appointments(self) -> List[Appointment]:
        """获取未来的预约列表
        
        Returns:
            List[Appointment]: 预约列表
        """
        appointments = self.get_all()
        today = datetime.now().strftime("%Y-%m-%d")
        
        return [appointment for appointment in appointments 
                if appointment.date >= today and appointment.is_scheduled()]
    
    def get_by_doctor_date_slot(self, doctor_id: int, date: str, time_slot: int) -> Optional[Appointment]:
        """根据医生ID、日期和时间槽获取预约
        
        Args:
            doctor_id (int): 医生ID
            date (str): 日期，格式为 "YYYY-MM-DD"
            time_slot (int): 时间槽索引
            
        Returns:
            Optional[Appointment]: 预约，如果不存在则返回None
        """
        appointments = self.get_all()
        
        for appointment in appointments:
            if (appointment.doctor_id == doctor_id and 
                appointment.date == date and 
                appointment.time_slot == time_slot and
                appointment.is_scheduled()):
                return appointment
        
        return None
    
    def is_slot_booked(self, doctor_id: int, date: str, time_slot: int) -> bool:
        """判断时间槽是否已被预约
        
        Args:
            doctor_id (int): 医生ID
            date (str): 日期，格式为 "YYYY-MM-DD"
            time_slot (int): 时间槽索引
            
        Returns:
            bool: 如果时间槽已被预约返回True，否则返回False
        """
        appointment = self.get_by_doctor_date_slot(doctor_id, date, time_slot)
        return appointment is not None
    
    def add_appointment(self, appointment: Appointment, update_schedule: bool = True) -> Appointment:
        """添加预约
        
        Args:
            appointment (Appointment): 预约实体
            update_schedule (bool, optional): 是否更新医生排班. 默认为 True，但已不再使用.
            
        Returns:
            Appointment: 添加的预约
        """
        # 首先检查时间槽是否可用
        if not self.is_slot_available(
            appointment.doctor_id, 
            appointment.clinic_id, 
            appointment.date, 
            appointment.time_slot
        ):
            raise ValueError("该时间槽不可用，可能已被预约或不在医生工作时间内")
        
        # 添加预约
        added_appointment = self.add(appointment)
        
        return added_appointment
    
    def cancel_appointment(self, appointment: Appointment, update_schedule: bool = True) -> bool:
        """取消预约
        
        Args:
            appointment (Appointment): 预约实体
            update_schedule (bool, optional): 是否更新医生排班. 默认为 True.
            
        Returns:
            bool: 如果取消成功返回True，否则返回False
        """
        # 更新预约状态
        if appointment.is_cancelled():
            return False
        
        # 取消预约
        appointment.cancel_by_patient()
        self.update(appointment)
        
        return True 

    def is_slot_available(self, doctor_id: int, clinic_id: int, date: str, time_slot: int) -> bool:
        """判断时间槽是否可用（在医生排班中可用且未被预约）
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            date (str): 日期，格式为 "YYYY-MM-DD"
            time_slot (int): 时间槽索引
            
        Returns:
            bool: 如果时间槽可用返回True，否则返回False
        """
        # 首先检查该时间槽是否已被预约
        if self.is_slot_booked(doctor_id, date, time_slot):
            return False
        
        # 然后检查该时间槽是否在医生排班中可用
        return self.__schedule_repo.is_slot_available(doctor_id, clinic_id, time_slot - 1) 
