#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File utility class, provides read/write functionality for CSV files
"""

import os
import csv
from typing import List, Dict, Any, Optional

class FileUtil:
    """File utility class, provides read/write functionality for CSV files"""
    
    @staticmethod
    def ensure_file_exists(file_path: str) -> None:
        """Ensure file exists, create an empty file if it doesn't exist
        
        Args:
            file_path (str): File path
        """
        if not os.path.exists(file_path):
            # Create directory
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # Create empty file
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                pass
    
    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, Any]]:
        """Read CSV file
        
        Args:
            file_path (str): File path
            
        Returns:
            List[Dict[str, Any]]: Data list, each element is a dictionary
        """
        FileUtil.ensure_file_exists(file_path)
        
        data = []
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames:  # Ensure file is not empty
                    for row in reader:
                        # Handle empty values
                        processed_row = {}
                        for key, value in row.items():
                            if value == '':
                                processed_row[key] = None
                            else:
                                processed_row[key] = value
                        data.append(processed_row)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            
        return data
    
    @staticmethod
    def write_csv(file_path: str, data: List[Dict[str, Any]]) -> bool:
        """Write to CSV file
        
        Args:
            file_path (str): File path
            data (List[Dict[str, Any]]): Data list, each element is a dictionary
            
        Returns:
            bool: Whether write was successful
        """
        FileUtil.ensure_file_exists(file_path)
        
        if not data:
            # If no data, create empty file
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                pass
            return True
        
        try:
            # Get all fields
            fieldnames = data[0].keys()
            
            # Write to CSV file
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            return True
        except Exception as e:
            print(f"Error writing to file {file_path}: {e}")
            return False
    
    @staticmethod
    def append_csv(file_path: str, row: Dict[str, Any]) -> bool:
        """Append a row of data to CSV file
        
        Args:
            file_path (str): File path
            row (Dict[str, Any]): Row data to append
            
        Returns:
            bool: Whether append was successful
        """
        FileUtil.ensure_file_exists(file_path)
        
        try:
            # Read existing data
            existing_data = FileUtil.read_csv(file_path)
            
            if not existing_data:
                # If file is empty, write directly
                return FileUtil.write_csv(file_path, [row])
            
            # Ensure field consistency
            for key in row.keys():
                if key not in existing_data[0]:
                    existing_data[0][key] = None
            
            for key in existing_data[0].keys():
                if key not in row:
                    row[key] = None
            
            # Append data
            existing_data.append(row)
            
            # Write back to file
            return FileUtil.write_csv(file_path, existing_data)
        except Exception as e:
            print(f"Error appending data to file {file_path}: {e}")
            return False
    
    @staticmethod
    def delete_row(file_path: str, condition: callable) -> bool:
        """Delete rows matching condition from CSV file
        
        Args:
            file_path (str): File path
            condition (callable): Condition function that takes a dictionary and returns a boolean
            
        Returns:
            bool: Whether deletion was successful
        """
        FileUtil.ensure_file_exists(file_path)
        
        try:
            # Read existing data
            existing_data = FileUtil.read_csv(file_path)
            
            if not existing_data:
                return True
            
            # Filter data
            filtered_data = [row for row in existing_data if not condition(row)]
            
            # If no rows were deleted, return directly
            if len(filtered_data) == len(existing_data):
                return True
            
            # Write back to file
            return FileUtil.write_csv(file_path, filtered_data)
        except Exception as e:
            print(f"Error deleting data from file {file_path}: {e}")
            return False
    
    @staticmethod
    def update_row(file_path: str, condition: callable, update_data: Dict[str, Any]) -> bool:
        """Update rows matching condition in CSV file
        
        Args:
            file_path (str): File path
            condition (callable): Condition function that takes a dictionary and returns a boolean
            update_data (Dict[str, Any]): Data to update
            
        Returns:
            bool: Whether update was successful
        """
        FileUtil.ensure_file_exists(file_path)
        
        try:
            # Read existing data
            existing_data = FileUtil.read_csv(file_path)
            
            if not existing_data:
                return True
            
            # Update data
            for row in existing_data:
                if condition(row):
                    for key, value in update_data.items():
                        row[key] = value
            
            # Write back to file
            return FileUtil.write_csv(file_path, existing_data)
        except Exception as e:
            print(f"Error updating data in file {file_path}: {e}")
            return False
    
    @staticmethod
    def get_next_id(file_path: str, id_field: str = 'id') -> int:
        """Get next available ID
        
        Args:
            file_path (str): File path
            id_field (str, optional): ID field name. Defaults to 'id'.
            
        Returns:
            int: Next available ID
        """
        FileUtil.ensure_file_exists(file_path)
        
        try:
            # Read existing data
            existing_data = FileUtil.read_csv(file_path)
            
            if not existing_data:
                return 1
            
            # Find maximum ID
            max_id = 0
            for row in existing_data:
                if id_field in row and row[id_field] is not None:
                    try:
                        row_id = int(row[id_field])
                        if row_id > max_id:
                            max_id = row_id
                    except (ValueError, TypeError):
                        pass
            
            return max_id + 1
        except Exception as e:
            print(f"Error getting next ID from file {file_path}: {e}")
            return 1 
