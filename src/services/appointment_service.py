#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Appointment Service Class - Handles business logic for appointments
"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

from src.entities.user import User
from src.entities.appointment import Appointment
from src.entities.notification import Notification
from src.repositories.appointment_repository import AppointmentRepository
from src.repositories.clinic_repository import ClinicRepository
from src.repositories.doctor_repository import DoctorRepository
from src.repositories.notification_repository import NotificationRepository
from src.repositories.doctor_schedule_repository import DoctorScheduleRepository
from src.repositories.user_repository import UserRepository
from src.utils.date_util import DateUtil


class AppointmentService:
    """Appointment Service Class - Handles business logic for appointments"""
    
    def __init__(self):
        """Initialize appointment service"""
        self.__appointment_repo = AppointmentRepository()
        self.__clinic_repo = ClinicRepository()
        self.__doctor_repo = DoctorRepository()
        self.__schedule_repo = DoctorScheduleRepository()
        self.__notification_repo = NotificationRepository()
        self.__user_repo = UserRepository()
    
    def get_all_clinics(self) -> List:
        """Get all clinics
        
        Returns:
            List: List of clinics
        """
        return self.__clinic_repo.get_all()
    
    def get_clinic_by_id(self, clinic_id: int):
        """Get clinic by ID
        
        Args:
            clinic_id (int): Clinic ID
            
        Returns:
            Clinic: Clinic object
        """
        return self.__clinic_repo.get_by_id(clinic_id)
    
    def get_all_doctors(self) -> List:
        """Get all doctors
        
        Returns:
            List: List of doctors
        """
        return self.__doctor_repo.get_all()
    
    def get_doctors_by_clinic(self, clinic_id: int) -> List:
        """Get doctors by clinic
        
        Args:
            clinic_id (int): Clinic ID
            
        Returns:
            List: List of doctors
        """
        return self.__doctor_repo.get_by_clinic(clinic_id)
    
    def get_doctor_by_id(self, doctor_id: int):
        """Get doctor by ID
        
        Args:
            doctor_id (int): Doctor ID
            
        Returns:
            Doctor: Doctor object
        """
        return self.__doctor_repo.get_by_id(doctor_id)
    
    def get_date_range(self, start_date: str, days: int) -> List[str]:
        """Get date range
        
        Args:
            start_date (str): Start date
            days (int): Number of days
            
        Returns:
            List[str]: List of dates
        """
        return DateUtil.get_date_range(start_date, days)
    
    def get_current_date(self) -> str:
        """Get current date
        
        Returns:
            str: Current date
        """
        return DateUtil.get_current_date()
    
    def get_day_of_week(self, date: str) -> str:
        """Get day of week
        
        Args:
            date (str): Date
            
        Returns:
            str: Day of week
        """
        return DateUtil.get_day_of_week(date)
    
    def is_valid_date(self, date_str: str) -> bool:
        """Check if date format is valid
        
        Args:
            date_str (str): Date string
            
        Returns:
            bool: Whether date format is valid
        """
        return DateUtil.is_valid_date(date_str)
    
    def get_time_slot_str(self, slot: int) -> str:
        """Get time slot string representation
        
        Args:
            slot (int): Time slot index
            
        Returns:
            str: Time slot string
        """
        return DateUtil.get_time_slot_str(slot)
    
    def get_available_time_slots(self, doctor_id: int, clinic_id: int, date: str) -> List[int]:
        """Get available time slots for a doctor at a clinic on a date
        
        Args:
            doctor_id (int): Doctor ID
            clinic_id (int): Clinic ID
            date (str): Date in YYYY-MM-DD format
            
        Returns:
            List[int]: List of available time slots
        """
        # Get doctor's schedule at the clinic
        doctor_schedule = self.__schedule_repo.get_by_doctor_clinic(doctor_id, clinic_id)
        
        # If no schedule found, create a default schedule with all time slots available
        if not doctor_schedule:
            doctor_schedule = self.__schedule_repo.create_default_schedule(doctor_id, clinic_id)
        
        # Get available time slots from doctor's schedule
        available_slots_base = DateUtil.hex_to_time_slots(doctor_schedule.time_slots)
        
        # If doctor has no available time slots, return empty list
        if not available_slots_base:
            return []
        
        # Check if each time slot in the schedule is available on that date
        available_slots = []
        for slot in available_slots_base:
            if self.__appointment_repo.is_slot_available(doctor_id, clinic_id, date, slot):
                available_slots.append(slot)
        
        return available_slots
    
    def get_available_slots_data(self, clinic_id: Optional[int] = None, 
                               doctor_id: Optional[int] = None, 
                               date: Optional[str] = None) -> List[Tuple]:
        """Get available time slots data
        
        Args:
            clinic_id (Optional[int]): Clinic ID
            doctor_id (Optional[int]): Doctor ID
            date (Optional[str]): Date
            
        Returns:
            List[Tuple]: List of tuples (date, time_slot, doctor_id, clinic_id, clinic_name, doctor_name, day_of_week, time_string)
        """
        # If date not specified, get dates for the next 7 days
        if date is None:
            today = DateUtil.get_current_date()
            future_dates = DateUtil.get_date_range(today, 7)
        else:
            future_dates = [date]
        
        # If clinic not specified, get all clinics
        if clinic_id is None:
            clinics = self.__clinic_repo.get_all()
            clinic_ids = [clinic.id for clinic in clinics]
        else:
            clinic_ids = [clinic_id]
        
        # If doctor not specified, get all doctors
        if doctor_id is None:
            doctors = self.__doctor_repo.get_all()
            doctor_ids = [doctor.id for doctor in doctors]
        else:
            doctor_ids = [doctor_id]
        
        available_slots_data = []
        
        # Iterate through all combinations
        for d_id in doctor_ids:
            doctor = self.__doctor_repo.get_by_id(d_id)
            if not doctor:
                continue
                
            for c_id in clinic_ids:
                # Check if doctor works at this clinic
                if c_id not in doctor.assigned_clinics:
                    continue
                    
                clinic = self.__clinic_repo.get_by_id(c_id)
                if not clinic:
                    continue
                    
                for date_str in future_dates:
                    day_of_week = DateUtil.get_day_of_week(date_str)
                    
                    # Get available time slots
                    available_slots = self.get_available_time_slots(d_id, c_id, date_str)
                    
                    if available_slots:
                        for slot in available_slots:
                            time_str = DateUtil.get_time_slot_str(slot)
                            available_slots_data.append(
                                (date_str, slot, d_id, c_id, clinic.name, doctor.full_name, day_of_week, time_str)
                            )
        
        return available_slots_data
    
    def make_appointment(self, user_id: int, doctor_id: int, clinic_id: int, 
                       date: str, time_slot: int, reason: str) -> Appointment:
        """Create an appointment
        
        Args:
            user_id (int): User ID
            doctor_id (int): Doctor ID
            clinic_id (int): Clinic ID
            date (str): Date
            time_slot (int): Time slot
            reason (str): Appointment reason
            
        Returns:
            Appointment: Created appointment
            
        Raises:
            ValueError: If time slot is not available
            ValueError: If appointment time is too soon (less than 2 hours in advance)
            ValueError: If user has another appointment at the same time
        """
        # Check if appointment is at least 2 hours in the future
        appointment_datetime = DateUtil.datetime_from_date_and_slot(date, time_slot)
        current_datetime = DateUtil.get_current_datetime()
        time_difference = appointment_datetime - current_datetime
        
        # Convert time difference to hours
        hours_difference = time_difference.total_seconds() / 3600
        
        # Check if appointment is at least 2 hours in the future
        if hours_difference < 2:
            raise ValueError("Appointments must be scheduled at least 2 hours in advance")
            
        # Check if user already has an appointment at the same time
        user_appointments = self.__appointment_repo.get_by_user(user_id)
        for existing_appointment in user_appointments:
            if existing_appointment.date == date and existing_appointment.time_slot == time_slot and existing_appointment.is_scheduled():
                raise ValueError("You already have another appointment scheduled at this time")
        
        # Create appointment record
        appointment = Appointment(
            user_id=user_id,
            doctor_id=doctor_id,
            clinic_id=clinic_id,
            date=date,
            time_slot=time_slot,
            reason=reason,
            status="Scheduled"
        )
        
        # Add appointment
        appointment = self.__appointment_repo.add_appointment(appointment)
        
        # Get related entities for notification
        doctor = self.__doctor_repo.get_by_id(doctor_id)
        clinic = self.__clinic_repo.get_by_id(clinic_id)
        
        # Create notification
        notification = Notification(
            user_id=user_id,
            message=f"You have successfully scheduled an appointment on {date} at {DateUtil.get_time_slot_str(time_slot)} with {doctor.full_name} at {clinic.name}.",
            date=DateUtil.get_current_date(),
            read=False
        )
        
        self.__notification_repo.add(notification)
        
        return appointment
    
    def get_user_appointments(self, user_id: int, future_only: bool = False, history_only: bool = False) -> List[Dict]:
        """Get user appointments
        
        Args:
            user_id (int): User ID
            future_only (bool): Whether to return only future appointments
            history_only (bool): Whether to return only past appointments
            
        Returns:
            List[Dict]: List of appointment information dictionaries
        """
        # Get appointments
        appointments = self.__appointment_repo.get_by_user(user_id)
        
        if not appointments:
            return []
        
        # Filter appointments
        today = DateUtil.get_current_date()
        filtered_appointments = []
        
        for appointment in appointments:
            if future_only and appointment.date < today:
                continue
            if history_only and appointment.date >= today:
                continue
            
            clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
            doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
            
            clinic_name = clinic.name if clinic else "Unknown Clinic"
            doctor_name = doctor.full_name if doctor else "Unknown Doctor"
            time_str = DateUtil.get_time_slot_str(appointment.time_slot)
            
            filtered_appointments.append({
                "id": appointment.id,
                "date": appointment.date,
                "time_slot": appointment.time_slot,
                "time_str": time_str,
                "clinic_id": appointment.clinic_id,
                "clinic_name": clinic_name,
                "doctor_id": appointment.doctor_id,
                "doctor_name": doctor_name,
                "reason": appointment.reason,
                "status": appointment.status,
                "appointment_obj": appointment  # Include original object for operations
            })
        
        return filtered_appointments
    
    def get_appointment_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Get appointment by ID
        
        Args:
            appointment_id (int): Appointment ID
            
        Returns:
            Optional[Appointment]: Appointment object, None if not found
        """
        return self.__appointment_repo.get_by_id(appointment_id)
    
    def get_appointment_details(self, appointment_id: int) -> Optional[Dict]:
        """Get appointment details
        
        Args:
            appointment_id (int): Appointment ID
            
        Returns:
            Optional[Dict]: Appointment details dictionary, None if not found
        """
        appointment = self.__appointment_repo.get_by_id(appointment_id)
        
        if not appointment:
            return None
        
        clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
        doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
        user = self.__user_repo.get_by_id(appointment.user_id)
        
        details = {
            "id": appointment.id,
            "user_id": appointment.user_id,
            "user_name": user.name if user else "Unknown User",
            "user_email": user.email if user else "Unknown Email",
            "date": appointment.date,
            "time_slot": appointment.time_slot,
            "time_str": DateUtil.get_time_slot_str(appointment.time_slot),
            "clinic_id": appointment.clinic_id,
            "clinic_name": clinic.name if clinic else "Unknown Clinic",
            "clinic_address": clinic.address if clinic else "Unknown Address",
            "doctor_id": appointment.doctor_id,
            "doctor_name": doctor.full_name if doctor else "Unknown Doctor",
            "reason": appointment.reason,
            "status": appointment.status,
            "can_cancel": appointment.is_scheduled() and appointment.date >= DateUtil.get_current_date(),
            "appointment_obj": appointment  # Include original object for operations
        }
        
        return details
    
    def cancel_appointment(self, appointment: Appointment) -> bool:
        """Cancel appointment
        
        Args:
            appointment (Appointment): Appointment object
            
        Returns:
            bool: Whether cancellation was successful
        """
        # Cancel appointment
        if self.__appointment_repo.cancel_appointment(appointment):
            # Create notification
            notification = Notification(
                user_id=appointment.user_id,
                message=f"You have cancelled your appointment on {appointment.date} at {DateUtil.get_time_slot_str(appointment.time_slot)}.",
                date=DateUtil.get_current_date(),
                read=False
            )
            
            self.__notification_repo.add(notification)
            
            return True
        
        return False
    
    def filter_appointments(self, user_id: int, params: Dict[str, Any]) -> List[Dict]:
        """Filter appointments
        
        Args:
            user_id (int): User ID
            params (Dict[str, Any]): Filter parameters
            
        Returns:
            List[Dict]: List of appointment information dictionaries
        """
        # Admin user (ID -1) can view all appointments
        if user_id == -1:
            appointments = self.__appointment_repo.get_all()
        else:
            # Regular users can only view their own appointments
            appointments = self.__appointment_repo.get_by_user(user_id)
        
        # Filter appointments
        filtered_appointments = []
        for appointment in appointments:
            if 'clinic_id' in params and params['clinic_id'] is not None and appointment.clinic_id != params['clinic_id']:
                continue
            if 'doctor_id' in params and params['doctor_id'] is not None and appointment.doctor_id != params['doctor_id']:
                continue
            if 'date' in params and params['date'] is not None and appointment.date != params['date']:
                continue
            
            clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
            doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
            
            clinic_name = clinic.name if clinic else "Unknown Clinic"
            doctor_name = doctor.full_name if doctor else "Unknown Doctor"
            time_str = DateUtil.get_time_slot_str(appointment.time_slot)
            
            filtered_appointments.append({
                "id": appointment.id,
                "user_id": appointment.user_id,
                "date": appointment.date,
                "time_slot": appointment.time_slot,
                "time_str": time_str,
                "clinic_id": appointment.clinic_id,
                "clinic_name": clinic_name,
                "doctor_id": appointment.doctor_id,
                "doctor_name": doctor_name,
                "reason": appointment.reason,
                "status": appointment.status,
                "appointment_obj": appointment  # Include original object for operations
            })
        
        return filtered_appointments

    def _show_all_appointments(self) -> None:
        """Display all appointments in the system (admin only)"""
        self.print_header("All Appointments")
        appointments = self.__appointment_service.get_all_appointments()

        if not appointments:
            print("No appointment records")
            self.wait_for_key()
            return

        print(f"{'ID':<5}{'User ID':<8}{'Date':<12}{'Time':<18}{'Doctor':<15}{'Clinic':<15}{'Status':<12}")
        print("-" * 90)
        for appt in appointments:
            print(f"{appt['id']:<5}{appt['user_id']:<8}{appt['date']:<12}{appt['time_str']:<18}"
                  f"{appt['doctor_name']:<15}{appt['clinic_name']:<15}{appt['status']:<12}")
        self.wait_for_key()

    def _cancel_by_id(self) -> None:
        """Admin manually cancels any appointment"""
        try:
            appt_id = int(input("\nEnter appointment ID to cancel (0 to return): ").strip())
            if appt_id == 0:
                return
            appointment = self.__appointment_service.get_appointment_by_id(appt_id)
            if not appointment or not appointment.is_scheduled():
                print("Appointment does not exist or cannot be cancelled")
                self.wait_for_key()
                return
            if input("Confirm cancellation? (Y/N): ").strip().upper() == "Y":
                if self.__appointment_service.cancel_appointment(appointment):
                    print("Cancelled")
                else:
                    print("Cancellation failed")
            else:
                print("Operation cancelled")
        except ValueError:
            print("Please enter a valid number")
        self.wait_for_key()

    def _search_as_admin(self) -> None:
        """Admin filters appointments (no user_id restriction)"""
        dummy_user = User(id=-1)  # Used to bypass user_id restriction
        self.search_appointments(dummy_user)

    def get_all_appointments(self) -> List[Dict]:
        """Get all appointments in the system (admin view)"""
        appointments = self.__appointment_repo.get_all()

        result = []
        for appointment in appointments:
            clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
            doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
            result.append({
                "id": appointment.id,
                "user_id": appointment.user_id,
                "date": appointment.date,
                "time_slot": appointment.time_slot,
                "time_str": DateUtil.get_time_slot_str(appointment.time_slot),
                "clinic_name": clinic.name if clinic else "Unknown",
                "doctor_name": doctor.full_name if doctor else "Unknown",
                "status": appointment.status
            })
        return result
