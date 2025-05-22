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
    
    def get_by_patient(self, patient_email: str) -> List[Appointment]:
        """根据患者电子邮箱获取预约列表
        
        Args:
            patient_email (str): 患者电子邮箱
            
        Returns:
            List[Appointment]: 预约列表
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.patient_email == patient_email]
    
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
        """添加预约并更新医生排班
        
        Args:
            appointment (Appointment): 预约实体
            update_schedule (bool, optional): 是否更新医生排班. 默认为 True.
            
        Returns:
            Appointment: 添加的预约
        """
        # 首先检查时间槽是否可用
        if self.is_slot_booked(appointment.doctor_id, appointment.date, appointment.time_slot):
            raise ValueError("该时间槽已被预约")
        
        # 添加预约
        added_appointment = self.add(appointment)
        
        # 如果需要，更新医生排班
        if update_schedule:
            self.__schedule_repo.set_slot_unavailable(
                appointment.doctor_id,
                appointment.clinic_id,
                appointment.time_slot - 1  # 医生排班的时间槽索引从0开始，预约的时间槽从1开始
            )
        
        return added_appointment
    
    def cancel_appointment(self, appointment: Appointment, update_schedule: bool = True) -> bool:
        """取消预约并更新医生排班
        
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
        
        # 如果需要，更新医生排班
        if update_schedule:
            self.__schedule_repo.set_slot_available(
                appointment.doctor_id,
                appointment.clinic_id,
                appointment.time_slot - 1  # 医生排班的时间槽索引从0开始，预约的时间槽从1开始
            )
        
        return True 
