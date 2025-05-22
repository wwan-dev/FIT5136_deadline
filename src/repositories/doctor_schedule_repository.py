#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
医生排班仓库类
"""

import os
from typing import List, Optional, Tuple
from datetime import datetime
from src.entities.doctor_schedule import DoctorSchedule
from src.repositories.base_repository import BaseRepository

class DoctorScheduleRepository(BaseRepository[DoctorSchedule]):
    """医生排班仓库类"""
    
    def __init__(self):
        """初始化医生排班仓库"""
        data_file = os.path.join("data", "doctor_schedules.csv")
        super().__init__(data_file, DoctorSchedule)
    
    def get_by_doctor_and_date(self, doctor_id: int, date: str) -> List[DoctorSchedule]:
        """根据医生ID和日期获取排班列表
        
        Args:
            doctor_id (int): 医生ID
            date (str): 日期，格式为 "YYYY-MM-DD"
            
        Returns:
            List[DoctorSchedule]: 排班列表
        """
        schedules = self.get_all()
        return [schedule for schedule in schedules 
                if schedule.doctor_id == doctor_id and schedule.date == date]
    
    def get_by_clinic_and_date(self, clinic_id: int, date: str) -> List[DoctorSchedule]:
        """根据诊所ID和日期获取排班列表
        
        Args:
            clinic_id (int): 诊所ID
            date (str): 日期，格式为 "YYYY-MM-DD"
            
        Returns:
            List[DoctorSchedule]: 排班列表
        """
        schedules = self.get_all()
        return [schedule for schedule in schedules 
                if schedule.clinic_id == clinic_id and schedule.date == date]
    
    def get_by_doctor_clinic_date(self, doctor_id: int, clinic_id: int, date: str) -> Optional[DoctorSchedule]:
        """根据医生ID、诊所ID和日期获取排班
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            date (str): 日期，格式为 "YYYY-MM-DD"
            
        Returns:
            Optional[DoctorSchedule]: 排班，如果不存在则返回None
        """
        schedules = self.get_all()
        
        for schedule in schedules:
            if (schedule.doctor_id == doctor_id and 
                schedule.clinic_id == clinic_id and 
                schedule.date == date):
                return schedule
        
        return None
    
    def get_available_slots(self, doctor_id: int, clinic_id: int, date: str) -> List[int]:
        """获取可用的时间槽列表
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            date (str): 日期，格式为 "YYYY-MM-DD"
            
        Returns:
            List[int]: 可用的时间槽索引列表
        """
        schedule = self.get_by_doctor_clinic_date(doctor_id, clinic_id, date)
        
        if not schedule or not schedule.time_slots:
            return []
        
        available_slots = []
        
        # 将16进制字符串转换为整数
        time_slots_int = int(schedule.time_slots, 16)
        
        # 检查每个时间槽
        for i in range(16):
            if time_slots_int & (1 << i):
                available_slots.append(i)
        
        return available_slots
    
    def is_slot_available(self, doctor_id: int, clinic_id: int, date: str, time_slot: int) -> bool:
        """判断时间槽是否可用
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            date (str): 日期，格式为 "YYYY-MM-DD"
            time_slot (int): 时间槽索引
            
        Returns:
            bool: 如果时间槽可用返回True，否则返回False
        """
        schedule = self.get_by_doctor_clinic_date(doctor_id, clinic_id, date)
        
        if not schedule:
            return False
        
        return schedule.is_available(time_slot)
    
    def set_slot_unavailable(self, doctor_id: int, clinic_id: int, date: str, time_slot: int) -> bool:
        """设置时间槽为不可用
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            date (str): 日期，格式为 "YYYY-MM-DD"
            time_slot (int): 时间槽索引
            
        Returns:
            bool: 如果设置成功返回True，否则返回False
        """
        schedule = self.get_by_doctor_clinic_date(doctor_id, clinic_id, date)
        
        if not schedule:
            return False
        
        schedule.set_unavailable(time_slot)
        self.update(schedule)
        
        return True
    
    def set_slot_available(self, doctor_id: int, clinic_id: int, date: str, time_slot: int) -> bool:
        """设置时间槽为可用
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            date (str): 日期，格式为 "YYYY-MM-DD"
            time_slot (int): 时间槽索引
            
        Returns:
            bool: 如果设置成功返回True，否则返回False
        """
        schedule = self.get_by_doctor_clinic_date(doctor_id, clinic_id, date)
        
        if not schedule:
            return False
        
        schedule.set_available(time_slot)
        self.update(schedule)
        
        return True
    
    def get_future_schedules(self) -> List[DoctorSchedule]:
        """获取未来的排班列表
        
        Returns:
            List[DoctorSchedule]: 排班列表
        """
        schedules = self.get_all()
        today = datetime.now().strftime("%Y-%m-%d")
        
        return [schedule for schedule in schedules if schedule.date >= today] 