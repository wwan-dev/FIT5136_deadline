#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Appointment Entity Class
"""

class Appointment:
    """<<Entity>> Appointment Entity Class"""
    
    def __init__(self, id=None, user_id=None, doctor_id=None, clinic_id=None, 
                 date=None, time_slot=None, reason=None, status=None, patient_email=None):
        """Initialize appointment entity
        
        Args:
            id (int, optional): Appointment ID
            user_id (int, optional): User ID
            doctor_id (int, optional): Doctor ID
            clinic_id (int, optional): Clinic ID
            date (str, optional): Date, format "YYYY-MM-DD"
            time_slot (int, optional): Time slot index (0-15)
            reason (str, optional): Appointment reason
            status (str, optional): Appointment status
            patient_email (str, optional): Patient email (for compatibility with old data)
        """
        self.__id = int(id) if id is not None else None
        # Handle compatibility: if patient_email is provided but no user_id, try to convert email to user_id
        if user_id is None and patient_email is not None:
            # Try to convert email to user ID
            if patient_email.isdigit():
                self.__user_id = int(patient_email)
            else:
                # Default to 1, in real application should query user repository
                self.__user_id = 1  
        else:
            self.__user_id = int(user_id) if user_id is not None else None
            
        self.__doctor_id = int(doctor_id) if doctor_id is not None else None
        self.__clinic_id = int(clinic_id) if clinic_id is not None else None
        self.__date = str(date) if date is not None else None
        self.__time_slot = int(time_slot) if time_slot is not None else None
        self.__reason = str(reason) if reason is not None else None
        self.__status = str(status) if status is not None else None
    
    # Accessor methods
    @property
    def id(self) -> int:
        """Get appointment ID
        
        Returns:
            int: Appointment ID
        """
        return self.__id
    
    @property
    def user_id(self) -> int:
        """Get user ID
        
        Returns:
            int: User ID
        """
        return self.__user_id
    
    @property
    def doctor_id(self) -> int:
        """Get doctor ID
        
        Returns:
            int: Doctor ID
        """
        return self.__doctor_id
    
    @property
    def clinic_id(self) -> int:
        """Get clinic ID
        
        Returns:
            int: Clinic ID
        """
        return self.__clinic_id
    
    @property
    def date(self) -> str:
        """Get date
        
        Returns:
            str: Date
        """
        return self.__date
    
    @property
    def time_slot(self) -> int:
        """Get time slot index
        
        Returns:
            int: Time slot index
        """
        return self.__time_slot
    
    @property
    def reason(self) -> str:
        """Get appointment reason
        
        Returns:
            str: Appointment reason
        """
        return self.__reason
    
    @property
    def status(self) -> str:
        """Get appointment status
        
        Returns:
            str: Appointment status
        """
        return self.__status
    
    # Property for backward compatibility
    @property
    def patient_email(self) -> str:
        """Get patient email (for backward compatibility)
        
        Returns:
            str: Patient email, now returns string representation of user ID
        """
        return str(self.__user_id)
    
    # Modifier methods
    @user_id.setter
    def user_id(self, user_id: int) -> None:
        """Set user ID
        
        Args:
            user_id (int): User ID
        """
        self.__user_id = int(user_id) if user_id is not None else None
    
    @doctor_id.setter
    def doctor_id(self, doctor_id: int) -> None:
        """Set doctor ID
        
        Args:
            doctor_id (int): Doctor ID
        """
        self.__doctor_id = int(doctor_id) if doctor_id is not None else None
    
    @clinic_id.setter
    def clinic_id(self, clinic_id: int) -> None:
        """Set clinic ID
        
        Args:
            clinic_id (int): Clinic ID
        """
        self.__clinic_id = int(clinic_id) if clinic_id is not None else None
    
    @date.setter
    def date(self, date: str) -> None:
        """Set date
        
        Args:
            date (str): Date
        """
        self.__date = str(date) if date is not None else None
    
    @time_slot.setter
    def time_slot(self, time_slot: int) -> None:
        """Set time slot index
        
        Args:
            time_slot (int): Time slot index
        """
        self.__time_slot = int(time_slot) if time_slot is not None else None
    
    @reason.setter
    def reason(self, reason: str) -> None:
        """Set appointment reason
        
        Args:
            reason (str): Appointment reason
        """
        self.__reason = str(reason) if reason is not None else None
    
    @status.setter
    def status(self, status: str) -> None:
        """Set appointment status
        
        Args:
            status (str): Appointment status
        """
        self.__status = str(status) if status is not None else None
    
    # Business methods
    def is_scheduled(self) -> bool:
        """Check if appointment is scheduled
        
        Returns:
            bool: True if appointment is scheduled, False otherwise
        """
        return self.__status == "Scheduled"
    
    def is_completed(self) -> bool:
        """Check if appointment is completed
        
        Returns:
            bool: True if appointment is completed, False otherwise
        """
        return self.__status == "Completed"
    
    def is_cancelled(self) -> bool:
        """Check if appointment is cancelled
        
        Returns:
            bool: True if appointment is cancelled, False otherwise
        """
        return self.__status == "Cancelled by Patient" or self.__status == "Cancelled by Clinic"
    
    def mark_as_scheduled(self) -> None:
        """Mark appointment as scheduled"""
        self.__status = "Scheduled"
    
    def mark_as_completed(self) -> None:
        """Mark appointment as completed"""
        self.__status = "Completed"
    
    def cancel_by_patient(self) -> None:
        """Cancel appointment by patient"""
        self.__status = "Cancelled by Patient"
    
    def cancel_by_clinic(self) -> None:
        """Cancel appointment by clinic"""
        self.__status = "Cancelled by Clinic"
    
    def __str__(self) -> str:
        """Return string representation of appointment
        
        Returns:
            str: String representation of appointment
        """
        return f"Appointment(id={self.__id}, user_id={self.__user_id}, doctor={self.__doctor_id}, date={self.__date}, time_slot={self.__time_slot}, status={self.__status})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary
        
        Returns:
            dict: Dictionary representation of appointment
        """
        return {
            "id": self.__id,
            "user_id": self.__user_id,
            "doctor_id": self.__doctor_id,
            "clinic_id": self.__clinic_id,
            "date": self.__date,
            "time_slot": self.__time_slot,
            "reason": self.__reason,
            "status": self.__status
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create appointment from dictionary
        
        Args:
            data (dict): Dictionary data of appointment
            
        Returns:
            Appointment: Appointment entity
        """
        # Handle field name changes, support for old data
        user_id = data.get("user_id")
        patient_email = data.get("patient_email")
        
        return cls(
            id=data.get("id"),
            user_id=user_id,
            patient_email=patient_email,  # For compatibility with old data
            doctor_id=data.get("doctor_id"),
            clinic_id=data.get("clinic_id"),
            date=data.get("date"),
            time_slot=data.get("time_slot"),
            reason=data.get("reason"),
            status=data.get("status")
        ) 
