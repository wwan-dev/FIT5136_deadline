#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
User Repository Class
"""

import os
from typing import List, Optional
from src.entities.user import User
from src.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    """User Repository Class"""
    
    def __init__(self):
        """Initialize user repository"""
        data_file = os.path.join("data", "users.csv")
        super().__init__(data_file, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email
        
        Args:
            email (str): User email
            
        Returns:
            Optional[User]: User if found, None otherwise
        """
        users = self.get_all()
        
        for user in users:
            if user.email == email:
                return user
        
        return None
    
    def get_patients(self) -> List[User]:
        """Get all patients
        
        Returns:
            List[User]: List of patients
        """
        users = self.get_all()
        return [user for user in users if user.is_patient()]
    
    def get_admins(self) -> List[User]:
        """Get all admins
        
        Returns:
            List[User]: List of admins
        """
        users = self.get_all()
        return [user for user in users if user.is_admin()]
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user login
        
        Args:
            email (str): User email
            password (str): User password
            
        Returns:
            Optional[User]: User if authentication successful, None otherwise
        """
        user = self.get_by_email(email)
        
        if user and user.password == password:
            return user
        
        return None

    # ─────────────────────────────────────────────
    # Save updated user information to users.csv
    # ─────────────────────────────────────────────
    def update_user(self, user: User) -> bool:
        """
        Use user.id as primary key to write the user row back to users.csv
        """
        from src.utils.file_util import FileUtil

        # Read current CSV file to get available field names
        existing_data = FileUtil.read_csv(self.data_file)
        if not existing_data:
            return False
        
        # Get field names from current CSV file
        available_fields = existing_data[0].keys()
        
        # Only keep fields that exist in CSV file
        user_dict = user.to_dict()
        update_data = {k: v for k, v in user_dict.items() if k in available_fields}
        
        return FileUtil.update_row(
            self.data_file,
            lambda row: row.get("id") == str(user.id),
            update_data
        )
