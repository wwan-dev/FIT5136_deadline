#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Doctor Schedule Repository Class
"""

import os
from typing import List, Optional, Tuple
from datetime import datetime
from src.entities.doctor_schedule import DoctorSchedule
from src.repositories.base_repository import BaseRepository
from src.utils.date_util import DateUtil

class DoctorScheduleRepository(BaseRepository[DoctorSchedule]):
    """Doctor Schedule Repository Class"""
    
    def __init__(self):
        """Initialize doctor schedule repository"""
        data_file = os.path.join("data", "doctor_schedules.csv")
        super().__init__(data_file, DoctorSchedule)
    
    def get_by_doctor(self, doctor_id: int) -> List[DoctorSchedule]:
        """Get schedules by doctor ID
        
        Args:
            doctor_id (int): Doctor ID
            
        Returns:
            List[DoctorSchedule]: List of schedules
        """
        schedules = self.get_all()
        return [schedule for schedule in schedules if schedule.doctor_id == doctor_id]
    
    def get_by_clinic(self, clinic_id: int) -> List[DoctorSchedule]:
        """Get schedules by clinic ID
        
        Args:
            clinic_id (int): Clinic ID
            
        Returns:
            List[DoctorSchedule]: List of schedules
        """
        schedules = self.get_all()
        return [schedule for schedule in schedules if schedule.clinic_id == clinic_id]
    
    def get_by_doctor_clinic(self, doctor_id: int, clinic_id: int) -> Optional[DoctorSchedule]:
        """Get schedule by doctor ID and clinic ID
        
        Args:
            doctor_id (int): Doctor ID
            clinic_id (int): Clinic ID
            
        Returns:
            Optional[DoctorSchedule]: Schedule if found, None otherwise
        """
        schedules = self.get_all()
        
        for schedule in schedules:
            if (schedule.doctor_id == doctor_id and schedule.clinic_id == clinic_id):
                return schedule
        
        return None
    
    def get_available_slots(self, doctor_id: int, clinic_id: int) -> List[int]:
        """Get available time slots
        
        Args:
            doctor_id (int): Doctor ID
            clinic_id (int): Clinic ID
            
        Returns:
            List[int]: List of available time slot indices
        """
        schedule = self.get_by_doctor_clinic(doctor_id, clinic_id)
        
        if not schedule or not schedule.time_slots:
            return []
        
        return DateUtil.hex_to_time_slots(schedule.time_slots)
    
    def is_slot_available(self, doctor_id: int, clinic_id: int, time_slot: int) -> bool:
        """Check if time slot is available in doctor's schedule
        
        Args:
            doctor_id (int): Doctor ID
            clinic_id (int): Clinic ID
            time_slot (int): Time slot index
            
        Returns:
            bool: True if time slot is available, False otherwise
        """
        schedule = self.get_by_doctor_clinic(doctor_id, clinic_id)
        
        if not schedule:
            return False
        
        return schedule.is_available(time_slot)
    
    def create_default_schedule(self, doctor_id: int, clinic_id: int) -> DoctorSchedule:
        """Create default schedule with all time slots available
        
        Args:
            doctor_id (int): Doctor ID
            clinic_id (int): Clinic ID
            
        Returns:
            DoctorSchedule: Created schedule
        """
        # Create a new schedule with all time slots available
        time_slots = DateUtil.time_slots_to_hex(list(range(1, 17)))
        schedule = DoctorSchedule(
            id=None,
            doctor_id=doctor_id, 
            clinic_id=clinic_id,
            time_slots=time_slots
        )
        return self.add(schedule)
    
    def get_all_schedules(self) -> List[DoctorSchedule]:
        """Get all schedules
        
        Returns:
            List[DoctorSchedule]: List of schedules
        """
        return self.get_all() 