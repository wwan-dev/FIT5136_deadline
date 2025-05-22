#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clinic Entity Class
"""

class Clinic:
    """<<Entity>> Clinic Entity Class"""
    
    def __init__(self, id=None, name=None, suburb=None, address=None, phone=None):
        """Initialize clinic entity
        
        Args:
            id (int, optional): Clinic ID
            name (str, optional): Clinic name
            suburb (str, optional): Suburb location
            address (str, optional): Address
            phone (str, optional): Phone number
        """
        self.__id = int(id) if id is not None else None
        self.__name = str(name) if name is not None else None
        self.__suburb = str(suburb) if suburb is not None else None
        self.__address = str(address) if address is not None else None
        self.__phone = str(phone) if phone is not None else None
    
    # Accessor methods
    @property
    def id(self) -> int:
        """Get clinic ID
        
        Returns:
            int: Clinic ID
        """
        return self.__id
    
    @property
    def name(self) -> str:
        """Get clinic name
        
        Returns:
            str: Clinic name
        """
        return self.__name
    
    @property
    def suburb(self) -> str:
        """Get clinic suburb
        
        Returns:
            str: Clinic suburb
        """
        return self.__suburb
    
    @property
    def address(self) -> str:
        """Get clinic address
        
        Returns:
            str: Clinic address
        """
        return self.__address
    
    @property
    def phone(self) -> str:
        """Get clinic phone number
        
        Returns:
            str: Clinic phone number
        """
        return self.__phone
    
    # Modifier methods
    @name.setter
    def name(self, name: str) -> None:
        """Set clinic name
        
        Args:
            name (str): Clinic name
        """
        self.__name = str(name) if name is not None else None
    
    @suburb.setter
    def suburb(self, suburb: str) -> None:
        """Set clinic suburb
        
        Args:
            suburb (str): Clinic suburb
        """
        self.__suburb = str(suburb) if suburb is not None else None
    
    @address.setter
    def address(self, address: str) -> None:
        """Set clinic address
        
        Args:
            address (str): Clinic address
        """
        self.__address = str(address) if address is not None else None
    
    @phone.setter
    def phone(self, phone: str) -> None:
        """Set clinic phone number
        
        Args:
            phone (str): Clinic phone number
        """
        self.__phone = str(phone) if phone is not None else None
    
    def __str__(self) -> str:
        """Return string representation of clinic
        
        Returns:
            str: String representation of clinic
        """
        return f"Clinic(id={self.__id}, name={self.__name}, suburb={self.__suburb})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary
        
        Returns:
            dict: Dictionary representation of clinic
        """
        return {
            "id": self.__id,
            "name": self.__name,
            "suburb": self.__suburb,
            "address": self.__address,
            "phone": self.__phone
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create clinic from dictionary
        
        Args:
            data (dict): Dictionary data of clinic
            
        Returns:
            Clinic: Clinic entity
        """
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            suburb=data.get("suburb"),
            address=data.get("address"),
            phone=data.get("phone")
        ) 