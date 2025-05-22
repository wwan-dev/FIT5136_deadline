#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Doctor Schedule Entity Class
"""

class DoctorSchedule:
    """<<Entity>> Doctor Schedule Entity Class"""
    
    def __init__(self, id=None, doctor_id=None, clinic_id=None, time_slots=None):
        """Initialize doctor schedule entity
        
        Args:
            id (int, optional): Schedule ID
            doctor_id (int, optional): Doctor ID
            clinic_id (int, optional): Clinic ID
            time_slots (str, optional): Time slots represented in hexadecimal
        """
        self.__id = int(id) if id is not None else None
        self.__doctor_id = int(doctor_id) if doctor_id is not None else None
        self.__clinic_id = int(clinic_id) if clinic_id is not None else None
        self.__time_slots = str(time_slots) if time_slots is not None else None
    
    # Accessor methods
    @property
    def id(self) -> int:
        """Get schedule ID
        
        Returns:
            int: Schedule ID
        """
        return self.__id
    
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
    def time_slots(self) -> str:
        """Get time slots
        
        Returns:
            str: Time slots represented in hexadecimal
        """
        return self.__time_slots
    
    # Modifier methods
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
    
    @time_slots.setter
    def time_slots(self, time_slots: str) -> None:
        """Set time slots
        
        Args:
            time_slots (str): Time slots represented in hexadecimal
        """
        self.__time_slots = str(time_slots) if time_slots is not None else None
    
    # Business methods
    def is_available(self, time_slot_index: int) -> bool:
        """Check if specified time slot is available
        
        Args:
            time_slot_index (int): Time slot index (0-15)
            
        Returns:
            bool: True if time slot is available, False otherwise
        """
        if not self.__time_slots:
            return False
        
        # Convert hexadecimal string to integer
        time_slots_int = int(self.__time_slots, 16)
        
        # Check if the corresponding bit is 1 (available)
        return (time_slots_int & (1 << time_slot_index)) != 0
    
    def set_available(self, time_slot_index: int) -> None:
        """Set specified time slot as available
        
        Args:
            time_slot_index (int): Time slot index (0-15)
        """
        if not self.__time_slots:
            self.__time_slots = "0"
        
        # Convert hexadecimal string to integer
        time_slots_int = int(self.__time_slots, 16)
        
        # Set the corresponding bit to 1 (available)
        time_slots_int |= (1 << time_slot_index)
        
        # Convert back to hexadecimal string
        self.__time_slots = format(time_slots_int, 'x')
    
    def set_unavailable(self, time_slot_index: int) -> None:
        """Set specified time slot as unavailable
        
        Args:
            time_slot_index (int): Time slot index (0-15)
        """
        if not self.__time_slots:
            return
        
        # Convert hexadecimal string to integer
        time_slots_int = int(self.__time_slots, 16)
        
        # Set the corresponding bit to 0 (unavailable)
        time_slots_int &= ~(1 << time_slot_index)
        
        # Convert back to hexadecimal string
        self.__time_slots = format(time_slots_int, 'x')
    
    def __str__(self) -> str:
        """Return string representation of doctor schedule
        
        Returns:
            str: String representation of doctor schedule
        """
        return f"DoctorSchedule(id={self.__id}, doctor_id={self.__doctor_id}, clinic_id={self.__clinic_id}, time_slots={self.__time_slots})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary
        
        Returns:
            dict: Dictionary representation of doctor schedule
        """
        return {
            "id": self.__id,
            "doctor_id": self.__doctor_id,
            "clinic_id": self.__clinic_id,
            "time_slots": self.__time_slots
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create doctor schedule from dictionary
        
        Args:
            data (dict): Dictionary data of doctor schedule
            
        Returns:
            DoctorSchedule: Doctor schedule entity
        """
        return cls(
            id=data.get("id"),
            doctor_id=data.get("doctor_id"),
            clinic_id=data.get("clinic_id"),
            time_slots=data.get("time_slots")
        ) 