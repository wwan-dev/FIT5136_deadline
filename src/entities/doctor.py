#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Doctor Entity Class
"""

from typing import List

class Doctor:
    """<<Entity>> Doctor Entity Class"""
    
    def __init__(self, id=None, full_name=None, email=None, assigned_clinics=None, specialisation=None):
        """Initialize doctor entity
        
        Args:
            id (int, optional): Doctor ID
            full_name (str, optional): Full name
            email (str, optional): Email address
            assigned_clinics (list, optional): List of assigned clinic IDs
            specialisation (list, optional): List of specialisations
        """
        self.__id = int(id) if id is not None else None
        self.__full_name = str(full_name) if full_name is not None else None
        self.__email = str(email) if email is not None else None
        self.__assigned_clinics = assigned_clinics if assigned_clinics else []
        self.__specialisation = specialisation if specialisation else []
    
    # Accessor methods
    @property
    def id(self) -> int:
        """Get doctor ID
        
        Returns:
            int: Doctor ID
        """
        return self.__id
    
    @property
    def full_name(self) -> str:
        """Get doctor full name
        
        Returns:
            str: Doctor full name
        """
        return self.__full_name
    
    @property
    def email(self) -> str:
        """Get doctor email
        
        Returns:
            str: Doctor email
        """
        return self.__email
    
    @property
    def assigned_clinics(self) -> List[int]:
        """Get list of assigned clinic IDs
        
        Returns:
            List[int]: List of assigned clinic IDs
        """
        return self.__assigned_clinics
    
    @property
    def specialisation(self) -> List[str]:
        """Get list of specialisations
        
        Returns:
            List[str]: List of specialisations
        """
        return self.__specialisation
    
    # Modifier methods
    @full_name.setter
    def full_name(self, full_name: str) -> None:
        """Set doctor full name
        
        Args:
            full_name (str): Doctor full name
        """
        self.__full_name = str(full_name) if full_name is not None else None
    
    @email.setter
    def email(self, email: str) -> None:
        """Set doctor email
        
        Args:
            email (str): Doctor email
        """
        self.__email = str(email) if email is not None else None
    
    @assigned_clinics.setter
    def assigned_clinics(self, assigned_clinics: List[int]) -> None:
        """Set list of assigned clinic IDs
        
        Args:
            assigned_clinics (List[int]): List of assigned clinic IDs
        """
        self.__assigned_clinics = assigned_clinics if assigned_clinics else []
    
    @specialisation.setter
    def specialisation(self, specialisation: List[str]) -> None:
        """Set list of specialisations
        
        Args:
            specialisation (List[str]): List of specialisations
        """
        self.__specialisation = specialisation if specialisation else []
    
    # Business methods
    def add_clinic(self, clinic_id: int) -> None:
        """Add clinic to doctor's assigned clinics
        
        Args:
            clinic_id (int): Clinic ID
        """
        if clinic_id not in self.__assigned_clinics:
            self.__assigned_clinics.append(clinic_id)
    
    def remove_clinic(self, clinic_id: int) -> None:
        """Remove clinic from doctor's assigned clinics
        
        Args:
            clinic_id (int): Clinic ID
        """
        if clinic_id in self.__assigned_clinics:
            self.__assigned_clinics.remove(clinic_id)
    
    def add_specialisation(self, specialisation: str) -> None:
        """Add specialisation to doctor's specialisations
        
        Args:
            specialisation (str): Specialisation
        """
        if specialisation not in self.__specialisation:
            self.__specialisation.append(specialisation)
    
    def remove_specialisation(self, specialisation: str) -> None:
        """Remove specialisation from doctor's specialisations
        
        Args:
            specialisation (str): Specialisation
        """
        if specialisation in self.__specialisation:
            self.__specialisation.remove(specialisation)
    
    def is_working_in_clinic(self, clinic_id: int) -> bool:
        """Check if doctor is working in specified clinic
        
        Args:
            clinic_id (int): Clinic ID
            
        Returns:
            bool: True if doctor is working in specified clinic, False otherwise
        """
        return clinic_id in self.__assigned_clinics
    
    def has_specialisation(self, specialisation: str) -> bool:
        """Check if doctor has specified specialisation
        
        Args:
            specialisation (str): Specialisation
            
        Returns:
            bool: True if doctor has specified specialisation, False otherwise
        """
        return specialisation in self.__specialisation
    
    def __str__(self) -> str:
        """Return string representation of doctor
        
        Returns:
            str: String representation of doctor
        """
        return f"Doctor(id={self.__id}, full_name={self.__full_name}, clinics={self.__assigned_clinics})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary
        
        Returns:
            dict: Dictionary representation of doctor
        """
        return {
            "id": self.__id,
            "full_name": self.__full_name,
            "email": self.__email,
            "assigned_clinics": self.__assigned_clinics,
            "specialisation": self.__specialisation
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create doctor from dictionary
        
        Args:
            data (dict): Dictionary data of doctor
            
        Returns:
            Doctor: Doctor entity
        """
        # Handle assigned_clinics field, which might be a string in the format "1;2;3"
        assigned_clinics = data.get("assigned_clinics")
        if isinstance(assigned_clinics, str):
            assigned_clinics = [int(clinic_id) for clinic_id in assigned_clinics.split(";") if clinic_id]
        
        # Handle specialisation field, which might be a string in the format "spec1;spec2"
        specialisation = data.get("specialisation")
        if isinstance(specialisation, str):
            specialisation = [spec.strip() for spec in specialisation.split(";") if spec]
        
        return cls(
            id=data.get("id"),
            full_name=data.get("full_name"),
            email=data.get("email"),
            assigned_clinics=assigned_clinics,
            specialisation=specialisation
        ) 
