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
from src.utils.date_util import DateUtil

class DoctorScheduleRepository(BaseRepository[DoctorSchedule]):
    """医生排班仓库类"""
    
    def __init__(self):
        """初始化医生排班仓库"""
        data_file = os.path.join("data", "doctor_schedules.csv")
        super().__init__(data_file, DoctorSchedule)
    
    def get_by_doctor(self, doctor_id: int) -> List[DoctorSchedule]:
        """根据医生ID获取排班列表
        
        Args:
            doctor_id (int): 医生ID
            
        Returns:
            List[DoctorSchedule]: 排班列表
        """
        schedules = self.get_all()
        return [schedule for schedule in schedules if schedule.doctor_id == doctor_id]
    
    def get_by_clinic(self, clinic_id: int) -> List[DoctorSchedule]:
        """根据诊所ID获取排班列表
        
        Args:
            clinic_id (int): 诊所ID
            
        Returns:
            List[DoctorSchedule]: 排班列表
        """
        schedules = self.get_all()
        return [schedule for schedule in schedules if schedule.clinic_id == clinic_id]
    
    def get_by_doctor_clinic(self, doctor_id: int, clinic_id: int) -> Optional[DoctorSchedule]:
        """根据医生ID和诊所ID获取排班
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            
        Returns:
            Optional[DoctorSchedule]: 排班，如果不存在则返回None
        """
        schedules = self.get_all()
        
        for schedule in schedules:
            if (schedule.doctor_id == doctor_id and schedule.clinic_id == clinic_id):
                return schedule
        
        return None
    
    def get_available_slots(self, doctor_id: int, clinic_id: int) -> List[int]:
        """获取可用的时间槽列表
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            
        Returns:
            List[int]: 可用的时间槽索引列表
        """
        schedule = self.get_by_doctor_clinic(doctor_id, clinic_id)
        
        if not schedule or not schedule.time_slots:
            return []
        
        return DateUtil.hex_to_time_slots(schedule.time_slots)
    
    def is_slot_available(self, doctor_id: int, clinic_id: int, time_slot: int) -> bool:
        """判断时间槽是否可用
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            time_slot (int): 时间槽索引
            
        Returns:
            bool: 如果时间槽可用返回True，否则返回False
        """
        schedule = self.get_by_doctor_clinic(doctor_id, clinic_id)
        
        if not schedule:
            return False
        
        return schedule.is_available(time_slot)
    
    def set_slot_unavailable(self, doctor_id: int, clinic_id: int, time_slot: int) -> bool:
        """设置时间槽为不可用
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            time_slot (int): 时间槽索引
            
        Returns:
            bool: 如果设置成功返回True，否则返回False
        """
        schedule = self.get_by_doctor_clinic(doctor_id, clinic_id)
        
        if not schedule:
            # 如果找不到，创建一个新排班，所有时间槽都可用
            time_slots = DateUtil.time_slots_to_hex(list(range(1, 17)))
            schedule = DoctorSchedule(
                id=None,
                doctor_id=doctor_id, 
                clinic_id=clinic_id,
                time_slots=time_slots
            )
            self.add(schedule)
        
        schedule.set_unavailable(time_slot)
        self.update(schedule)
        
        return True
    
    def set_slot_available(self, doctor_id: int, clinic_id: int, time_slot: int) -> bool:
        """设置时间槽为可用
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            time_slot (int): 时间槽索引
            
        Returns:
            bool: 如果设置成功返回True，否则返回False
        """
        schedule = self.get_by_doctor_clinic(doctor_id, clinic_id)
        
        if not schedule:
            # 如果找不到，创建一个新排班，所有时间槽都可用
            time_slots = DateUtil.time_slots_to_hex(list(range(1, 17)))
            schedule = DoctorSchedule(
                id=None,
                doctor_id=doctor_id, 
                clinic_id=clinic_id,
                time_slots=time_slots
            )
            self.add(schedule)
        
        schedule.set_available(time_slot)
        self.update(schedule)
        
        return True
    
    def get_future_schedules(self) -> List[DoctorSchedule]:
        """获取未来的排班列表
        
        Returns:
            List[DoctorSchedule]: 排班列表
        """
        # 返回所有排班，因为排班不再与日期相关联
        return self.get_all() 