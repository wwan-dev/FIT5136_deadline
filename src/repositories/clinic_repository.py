#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clinic Repository Class
"""

import os
from typing import List, Optional
from src.entities.clinic import Clinic
from src.repositories.base_repository import BaseRepository

class ClinicRepository(BaseRepository[Clinic]):
    """Clinic Repository Class"""
    
    def __init__(self):
        """Initialize clinic repository"""
        data_file = os.path.join("data", "clinics.csv")
        super().__init__(data_file, Clinic)
    
    def get_by_suburb(self, suburb: str) -> List[Clinic]:
        """Get clinics by suburb
        
        Args:
            suburb (str): Suburb name
            
        Returns:
            List[Clinic]: List of clinics
        """
        clinics = self.get_all()
        return [clinic for clinic in clinics if clinic.suburb.lower() == suburb.lower()]
    
    def get_by_name(self, name: str) -> Optional[Clinic]:
        """Get clinic by name
        
        Args:
            name (str): Clinic name
            
        Returns:
            Optional[Clinic]: Clinic if found, None otherwise
        """
        clinics = self.get_all()
        
        for clinic in clinics:
            if clinic.name.lower() == name.lower():
                return clinic
        
        return None
    
    def search(self, keyword: str) -> List[Clinic]:
        """Search clinics
        
        Args:
            keyword (str): Search keyword
            
        Returns:
            List[Clinic]: List of matching clinics
        """
        clinics = self.get_all()
        keyword = keyword.lower()
        
        return [clinic for clinic in clinics if 
                keyword in clinic.name.lower() or 
                keyword in clinic.suburb.lower() or 
                keyword in clinic.address.lower()] 