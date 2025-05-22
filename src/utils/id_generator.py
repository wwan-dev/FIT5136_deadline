#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ID Generator utility class, used to generate unique identifiers for entities
"""

import os
import csv
from typing import Dict, Optional

class IdGenerator:
    """ID Generator utility class, used to generate unique identifiers for entities"""
    
    # Store maximum ID values for each entity type
    __max_ids: Dict[str, int] = {}
    
    @classmethod
    def initialize(cls, data_dir: str = "data") -> None:
        """Initialize ID generator, get maximum ID for each entity type
        
        Args:
            data_dir (str, optional): Data directory. Defaults to "data".
        """
        # Ensure data directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Initialize maximum ID dictionary
        cls.__max_ids = {}
        
        # Find all CSV files in the data directory
        for filename in os.listdir(data_dir):
            if filename.endswith(".csv"):
                entity_type = filename.replace(".csv", "")
                file_path = os.path.join(data_dir, filename)
                
                # Initialize maximum ID to 0
                max_id = 0
                
                # Read CSV file to get maximum ID
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            if 'id' in row and row['id']:
                                try:
                                    id_value = int(row['id'])
                                    max_id = max(max_id, id_value)
                                except (ValueError, TypeError):
                                    pass
                
                # Save maximum ID value
                cls.__max_ids[entity_type] = max_id
    
    @classmethod
    def next_id(cls, entity_type: str) -> int:
        """Get the next available ID for the specified entity type
        
        Args:
            entity_type (str): Entity type name (e.g., "users", "clinics", "doctors", "doctor_schedules", "appointments", "notifications")
            
        Returns:
            int: Next available ID
            
        Raises:
            ValueError: If the ID generator is not initialized
        """
        # If not initialized, initialize first
        if not cls.__max_ids:
            cls.initialize()
        
        # Get current maximum ID for the entity type
        max_id = cls.__max_ids.get(entity_type, 0)
        
        # Generate next ID
        next_id = max_id + 1
        
        # Update maximum ID record
        cls.__max_ids[entity_type] = next_id
        
        return next_id
    
    @classmethod
    def get_max_id(cls, entity_type: str) -> int:
        """Get current maximum ID for the specified entity type
        
        Args:
            entity_type (str): Entity type name
            
        Returns:
            int: Current maximum ID, returns 0 if entity type doesn't exist
        """
        # If not initialized, initialize first
        if not cls.__max_ids:
            cls.initialize()
            
        return cls.__max_ids.get(entity_type, 0) 