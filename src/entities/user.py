#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
User Entity Class
"""

class User:
    """<<Entity>> User Entity Class"""
    
    def __init__(self, id=None, email=None, password=None, role=None, name=None, phone=None, address=None,
                 date_of_birth=None, gender=None, medical_history=None):
        """Initialize user entity
        
        Args:
            id (int, optional): User ID
            email (str, optional): Email address
            password (str, optional): Password
            role (str, optional): Role (patient/admin)
            name (str, optional): Name
            phone (str, optional): Phone number
            address (str, optional): Address
            date_of_birth (str, optional): Date of birth, format "YYYY-MM-DD", only required for patients
            gender (str, optional): Gender, only required for patients
            medical_history (str, optional): Medical history, only required for patients
        """
        self.__id = int(id) if id is not None else None
        self.__email = str(email) if email is not None else None
        self.__password = str(password) if password is not None else None
        self.__role = str(role) if role is not None else None
        self.__name = str(name) if name is not None else None
        self.__phone = str(phone) if phone is not None else None
        self.__address = str(address) if address is not None else None
        self.__date_of_birth = str(date_of_birth) if date_of_birth is not None else None
        self.__gender = str(gender) if gender is not None else None
        self.__medical_history = str(medical_history) if medical_history is not None else None
    
    # Accessor methods
    @property
    def id(self) -> int:
        """Get user ID
        
        Returns:
            int: User ID
        """
        return self.__id
    
    @property
    def email(self) -> str:
        """Get user email
        
        Returns:
            str: User email
        """
        return self.__email
    
    @property
    def password(self) -> str:
        """Get user password
        
        Returns:
            str: User password
        """
        return self.__password
    
    @property
    def role(self) -> str:
        """Get user role
        
        Returns:
            str: User role
        """
        return self.__role
    
    @property
    def name(self) -> str:
        """Get user name
        
        Returns:
            str: User name
        """
        return self.__name
    
    @property
    def phone(self) -> str:
        """Get user phone number
        
        Returns:
            str: User phone number
        """
        return self.__phone
    
    @property
    def address(self) -> str:
        """Get user address
        
        Returns:
            str: User address
        """
        return self.__address
    
    @property
    def date_of_birth(self) -> str:
        """Get user date of birth
        
        Returns:
            str: User date of birth
        """
        return self.__date_of_birth
    
    @property
    def gender(self) -> str:
        """Get user gender
        
        Returns:
            str: User gender
        """
        return self.__gender
    
    @property
    def medical_history(self) -> str:
        """Get user medical history
        
        Returns:
            str: User medical history
        """
        return self.__medical_history
    
    # Modifier methods
    @email.setter
    def email(self, email: str) -> None:
        """Set user email
        
        Args:
            email (str): User email
        """
        self.__email = str(email) if email is not None else None
    
    @password.setter
    def password(self, password: str) -> None:
        """Set user password
        
        Args:
            password (str): User password
        """
        self.__password = str(password) if password is not None else None
    
    @role.setter
    def role(self, role: str) -> None:
        """Set user role
        
        Args:
            role (str): User role
        """
        self.__role = str(role) if role is not None else None
    
    @name.setter
    def name(self, name: str) -> None:
        """Set user name
        
        Args:
            name (str): User name
        """
        self.__name = str(name) if name is not None else None
    
    @phone.setter
    def phone(self, phone: str) -> None:
        """Set user phone number
        
        Args:
            phone (str): User phone number
        """
        self.__phone = str(phone) if phone is not None else None
    
    @address.setter
    def address(self, address: str) -> None:
        """Set user address
        
        Args:
            address (str): User address
        """
        self.__address = str(address) if address is not None else None
    
    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: str) -> None:
        """Set user date of birth
        
        Args:
            date_of_birth (str): User date of birth
        """
        self.__date_of_birth = str(date_of_birth) if date_of_birth is not None else None
    
    @gender.setter
    def gender(self, gender: str) -> None:
        """Set user gender
        
        Args:
            gender (str): User gender
        """
        self.__gender = str(gender) if gender is not None else None
    
    @medical_history.setter
    def medical_history(self, medical_history: str) -> None:
        """Set user medical history
        
        Args:
            medical_history (str): User medical history
        """
        self.__medical_history = str(medical_history) if medical_history is not None else None
    
    # Business methods
    def is_admin(self) -> bool:
        """Check if user is an admin
        
        Returns:
            bool: True if user is an admin, False otherwise
        """
        return self.__role == "admin"
    
    def is_patient(self) -> bool:
        """Check if user is a patient
        
        Returns:
            bool: True if user is a patient, False otherwise
        """
        return self.__role == "patient"
    
    def __str__(self) -> str:
        """Return string representation of user
        
        Returns:
            str: String representation of user
        """
        if self.is_patient():
            return f"User(id={self.__id}, email={self.__email}, role={self.__role}, name={self.__name}, gender={self.__gender})"
        else:
            return f"User(id={self.__id}, email={self.__email}, role={self.__role}, name={self.__name})"
    
    def to_dict(self) -> dict:
        """Convert to dictionary
        
        Returns:
            dict: Dictionary representation of user
        """
        data = {
            "id": self.__id,
            "email": self.__email,
            "password": self.__password,
            "role": self.__role,
            "name": self.__name,
            "phone": self.__phone,
            "address": self.__address
        }
        
        # Only add patient-specific fields if user is a patient
        if self.is_patient():
            data.update({
                "date_of_birth": self.__date_of_birth,
                "gender": self.__gender,
                "medical_history": self.__medical_history
            })
            
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create user from dictionary
        
        Args:
            data (dict): Dictionary data of user
            
        Returns:
            User: User entity
        """
        return cls(
            id=data.get("id"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role"),
            name=data.get("name"),
            phone=data.get("phone"),
            address=data.get("address"),
            date_of_birth=data.get("date_of_birth"),
            gender=data.get("gender"),
            medical_history=data.get("medical_history")
        ) 
