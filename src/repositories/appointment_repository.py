#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Appointment Repository Class
"""

import os
from typing import List, Optional
from datetime import datetime
from src.entities.appointment import Appointment
from src.repositories.base_repository import BaseRepository
from src.repositories.doctor_schedule_repository import DoctorScheduleRepository

class AppointmentRepository(BaseRepository[Appointment]):
    """Appointment Repository Class"""
    
    def __init__(self):
        """Initialize appointment repository"""
        data_file = os.path.join("data", "appointments.csv")
        super().__init__(data_file, Appointment)
        self.__schedule_repo = DoctorScheduleRepository()
    
    def get_by_user(self, user_id: int) -> List[Appointment]:
        """Get appointments by user ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            List[Appointment]: List of appointments
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.user_id == user_id]
    
    # Compatible with legacy code
    def get_by_patient(self, patient_email: str) -> List[Appointment]:
        """Get appointments by patient email (compatible with legacy code)
        
        Args:
            patient_email (str): Patient email or user ID
            
        Returns:
            List[Appointment]: List of appointments
        """
        # If parameter is a number, treat it as user ID
        if isinstance(patient_email, int) or (isinstance(patient_email, str) and patient_email.isdigit()):
            user_id = int(patient_email)
            return self.get_by_user(user_id)
            
        # Otherwise, need to find the corresponding user ID from user repository
        from src.repositories.user_repository import UserRepository
        user_repo = UserRepository()
        users = user_repo.get_all()
        
        for user in users:
            if user.email == patient_email:
                return self.get_by_user(user.id)
        
        # If no matching user is found, return empty list
        return []
    
    def get_by_doctor(self, doctor_id: int) -> List[Appointment]:
        """Get appointments by doctor ID
        
        Args:
            doctor_id (int): Doctor ID
            
        Returns:
            List[Appointment]: List of appointments
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.doctor_id == doctor_id]
    
    def get_by_clinic(self, clinic_id: int) -> List[Appointment]:
        """Get appointments by clinic ID
        
        Args:
            clinic_id (int): Clinic ID
            
        Returns:
            List[Appointment]: List of appointments
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.clinic_id == clinic_id]
    
    def get_by_date(self, date: str) -> List[Appointment]:
        """Get appointments by date
        
        Args:
            date (str): Date in format "YYYY-MM-DD"
            
        Returns:
            List[Appointment]: List of appointments
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.date == date]
    
    def get_scheduled_appointments(self) -> List[Appointment]:
        """Get list of scheduled appointments
        
        Returns:
            List[Appointment]: List of appointments
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.is_scheduled()]
    
    def get_completed_appointments(self) -> List[Appointment]:
        """Get list of completed appointments
        
        Returns:
            List[Appointment]: List of appointments
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.is_completed()]
    
    def get_cancelled_appointments(self) -> List[Appointment]:
        """Get list of cancelled appointments
        
        Returns:
            List[Appointment]: List of appointments
        """
        appointments = self.get_all()
        return [appointment for appointment in appointments if appointment.is_cancelled()]
    
    def get_future_appointments(self) -> List[Appointment]:
        """Get list of future appointments
        
        Returns:
            List[Appointment]: List of appointments
        """
        appointments = self.get_all()
        today = datetime.now().strftime("%Y-%m-%d")
        
        return [appointment for appointment in appointments 
                if appointment.date >= today and appointment.is_scheduled()]
    
    def get_by_doctor_date_slot(self, doctor_id: int, date: str, time_slot: int) -> Optional[Appointment]:
        """Get appointment by doctor ID, date and time slot
        
        Args:
            doctor_id (int): Doctor ID
            date (str): Date in format "YYYY-MM-DD"
            time_slot (int): Time slot index
            
        Returns:
            Optional[Appointment]: Appointment if exists, None otherwise
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
        """Check if time slot is already booked
        
        Args:
            doctor_id (int): Doctor ID
            date (str): Date in format "YYYY-MM-DD"
            time_slot (int): Time slot index
            
        Returns:
            bool: True if time slot is booked, False otherwise
        """
        appointment = self.get_by_doctor_date_slot(doctor_id, date, time_slot)
        return appointment is not None
    
    def add_appointment(self, appointment: Appointment, update_schedule: bool = True) -> Appointment:
        """Add appointment
        
        Args:
            appointment (Appointment): Appointment entity
            update_schedule (bool, optional): Whether to update doctor schedule. Defaults to True, but no longer used.
            
        Returns:
            Appointment: Added appointment
        """
        # First check if time slot is available
        if not self.is_slot_available(
            appointment.doctor_id, 
            appointment.clinic_id, 
            appointment.date, 
            appointment.time_slot
        ):
            raise ValueError("This time slot is not available, it may be already booked or not within doctor's working hours")
        
        # Add appointment
        added_appointment = self.add(appointment)
        
        return added_appointment
    
    def cancel_appointment(self, appointment: Appointment, update_schedule: bool = True) -> bool:
        """Cancel appointment
        
        Args:
            appointment (Appointment): Appointment entity
            update_schedule (bool, optional): Whether to update doctor schedule. Defaults to True.
            
        Returns:
            bool: True if cancellation was successful, False otherwise
        """
        # Update appointment status
        if appointment.is_cancelled():
            return False
        
        # Cancel appointment
        appointment.cancel_by_patient()
        self.update(appointment)
        
        return True 

    def is_slot_available(self, doctor_id: int, clinic_id: int, date: str, time_slot: int) -> bool:
        """Check if time slot is available (available in doctor's schedule and not booked)
        
        Args:
            doctor_id (int): Doctor ID
            clinic_id (int): Clinic ID
            date (str): Date in format "YYYY-MM-DD"
            time_slot (int): Time slot index
            
        Returns:
            bool: True if time slot is available, False otherwise
        """
        # First check if time slot is already booked
        if self.is_slot_booked(doctor_id, date, time_slot):
            return False
        
        # Then check if time slot is available in doctor's schedule
        return self.__schedule_repo.is_slot_available(doctor_id, clinic_id, time_slot - 1) 
