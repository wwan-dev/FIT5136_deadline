#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Base Repository Class
"""

import os
from typing import List, Dict, Any, TypeVar, Generic, Type, Optional
from src.utils.file_util import FileUtil
from src.utils.id_generator import IdGenerator

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """Base repository class, provides generic CRUD operations"""
    
    def __init__(self, data_file: str, entity_class: Type[T]):
        """Initialize repository
        
        Args:
            data_file (str): Data file path
            entity_class (Type[T]): Entity class
        """
        self.data_file = data_file
        self.entity_class = entity_class
        
        # Ensure data file exists
        FileUtil.ensure_file_exists(data_file)
        
        # Get entity type
        file_name = os.path.basename(data_file)
        self.entity_type = os.path.splitext(file_name)[0]
    
    def get_all(self) -> List[T]:
        """Get all entities
        
        Returns:
            List[T]: List of entities
        """
        entities = []
        
        # Read CSV file
        rows = FileUtil.read_csv(self.data_file)
        
        # Convert to entity objects
        for row in rows:
            entity = self.entity_class.from_dict(row)
            entities.append(entity)
        
        return entities
    
    def get_by_id(self, entity_id) -> Optional[T]:
        """Get entity by ID
        
        Args:
            entity_id: Entity ID
            
        Returns:
            Optional[T]: Entity, returns None if not found
        """
        entities = self.get_all()
        
        for entity in entities:
            if str(entity.id) == str(entity_id):
                return entity
        
        return None
    
    def add(self, entity: T) -> T:
        """Add entity
        
        Args:
            entity (T): Entity to add
            
        Returns:
            T: Added entity
        """
        # If new entity, generate ID using IdGenerator
        if entity.id is None:
            # Use entity_type to generate ID
            next_id = IdGenerator.next_id(self.entity_type)
            
            # Since entity class doesn't have id setter, use reflection to set id attribute
            # Assuming entity class's id is stored in _Entity__id (Python name mangling)
            setattr(entity, f"_{entity.__class__.__name__}__id", next_id)
        
        # Convert entity to dictionary
        entity_dict = entity.to_dict()
        
        # Convert lists to semicolon-separated strings (for CSV storage)
        for key, value in entity_dict.items():
            if isinstance(value, list):
                entity_dict[key] = ";".join([str(item) for item in value])
        
        # Append to CSV file
        FileUtil.append_csv(self.data_file, entity_dict)
        
        return entity
    
    def update(self, entity: T) -> T:
        """Update entity
        
        Args:
            entity (T): Entity to update
            
        Returns:
            T: Updated entity
        """
        # Convert entity to dictionary
        entity_dict = entity.to_dict()
        
        # Convert lists to semicolon-separated strings (for CSV storage)
        for key, value in entity_dict.items():
            if isinstance(value, list):
                entity_dict[key] = ";".join([str(item) for item in value])
        
        # Update row in CSV file
        FileUtil.update_row(
            self.data_file,
            lambda row: str(row.get('id')) == str(entity.id),
            entity_dict
        )
        
        return entity
    
    def delete(self, entity_id) -> bool:
        """Delete entity
        
        Args:
            entity_id: Entity ID
            
        Returns:
            bool: Whether deletion was successful
        """
        # Delete row from CSV file
        return FileUtil.delete_row(
            self.data_file,
            lambda row: str(row.get('id')) == str(entity_id)
        )
    
    def _save_all(self, entities: List[T]) -> None:
        """Save all entities to file
        
        Args:
            entities (List[T]): List of entities
        """
        # Convert entities to dictionaries
        rows = [entity.to_dict() for entity in entities]
        
        # Write to CSV file
        FileUtil.write_csv(self.data_file, rows) 