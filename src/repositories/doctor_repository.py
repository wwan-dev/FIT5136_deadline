#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Doctor Repository Class
"""

import os
from typing import List, Optional
from src.entities.doctor import Doctor
from src.repositories.base_repository import BaseRepository

class DoctorRepository(BaseRepository[Doctor]):
    """Doctor Repository Class"""
    
    def __init__(self):
        """Initialize doctor repository"""
        data_file = os.path.join("data", "doctors.csv")
        super().__init__(data_file, Doctor)
    
    def get_by_clinic(self, clinic_id: int) -> List[Doctor]:
        """Get doctors by clinic ID
        
        Args:
            clinic_id (int): Clinic ID
            
        Returns:
            List[Doctor]: List of doctors
        """
        doctors = self.get_all()
        return [doctor for doctor in doctors if doctor.is_working_in_clinic(clinic_id)]
    
    def get_by_specialisation(self, specialisation: str) -> List[Doctor]:
        """Get doctors by specialisation
        
        Args:
            specialisation (str): Specialisation
            
        Returns:
            List[Doctor]: List of doctors
        """
        doctors = self.get_all()
        return [doctor for doctor in doctors if doctor.has_specialisation(specialisation)]
    
    def get_by_email(self, email: str) -> Optional[Doctor]:
        """Get doctor by email
        
        Args:
            email (str): Doctor's email
            
        Returns:
            Optional[Doctor]: Doctor if found, None otherwise
        """
        doctors = self.get_all()
        
        for doctor in doctors:
            if doctor.email == email:
                return doctor
        
        return None
    
    def search(self, keyword: str) -> List[Doctor]:
        """Search doctors
        
        Args:
            keyword (str): Search keyword
            
        Returns:
            List[Doctor]: List of matching doctors
        """
        doctors = self.get_all()
        keyword = keyword.lower()
        
        result = []
        for doctor in doctors:
            if keyword in doctor.full_name.lower() or keyword in doctor.email.lower():
                result.append(doctor)
                continue
            
            # Check specialisation
            for spec in doctor.specialisation:
                if keyword in spec.lower():
                    result.append(doctor)
                    break
        
        return result 
