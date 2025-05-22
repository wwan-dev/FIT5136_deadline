#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
基础仓库类
"""

import csv
import os
from typing import List, Dict, Any, TypeVar, Generic, Type, Optional

T = TypeVar('T')

class BaseRepository(Generic[T]):
    """基础仓库类，提供通用的CRUD操作"""
    
    def __init__(self, data_file: str, entity_class: Type[T]):
        """初始化仓库
        
        Args:
            data_file (str): 数据文件路径
            entity_class (Type[T]): 实体类
        """
        self.data_file = data_file
        self.entity_class = entity_class
        
        # 确保数据文件存在
        if not os.path.exists(data_file):
            # 创建目录
            os.makedirs(os.path.dirname(data_file), exist_ok=True)
            # 创建空文件
            with open(data_file, 'w', newline='', encoding='utf-8') as f:
                pass
    
    def get_all(self) -> List[T]:
        """获取所有实体
        
        Returns:
            List[T]: 实体列表
        """
        entities = []
        
        try:
            with open(self.data_file, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames:  # 确保文件不为空
                    for row in reader:
                        entity = self.entity_class.from_dict(row)
                        entities.append(entity)
        except FileNotFoundError:
            # 文件不存在时返回空列表
            pass
        
        return entities
    
    def get_by_id(self, entity_id) -> Optional[T]:
        """根据ID获取实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            Optional[T]: 实体，如果不存在则返回None
        """
        entities = self.get_all()
        
        for entity in entities:
            if str(entity.id) == str(entity_id):
                return entity
        
        return None
    
    def add(self, entity: T) -> T:
        """添加实体
        
        Args:
            entity (T): 要添加的实体
            
        Returns:
            T: 添加后的实体
        """
        entities = self.get_all()
        
        # 如果是新实体，生成ID
        if entity.id is None:
            max_id = 0
            for e in entities:
                if e.id is not None and int(e.id) > max_id:
                    max_id = int(e.id)
            entity.id = max_id + 1
        
        # 添加实体
        entities.append(entity)
        
        # 保存到文件
        self._save_all(entities)
        
        return entity
    
    def update(self, entity: T) -> T:
        """更新实体
        
        Args:
            entity (T): 要更新的实体
            
        Returns:
            T: 更新后的实体
        """
        entities = self.get_all()
        
        for i, e in enumerate(entities):
            if str(e.id) == str(entity.id):
                entities[i] = entity
                break
        
        # 保存到文件
        self._save_all(entities)
        
        return entity
    
    def delete(self, entity_id) -> bool:
        """删除实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            bool: 是否删除成功
        """
        entities = self.get_all()
        original_count = len(entities)
        
        entities = [e for e in entities if str(e.id) != str(entity_id)]
        
        if len(entities) < original_count:
            # 保存到文件
            self._save_all(entities)
            return True
        
        return False
    
    def _save_all(self, entities: List[T]) -> None:
        """保存所有实体到文件
        
        Args:
            entities (List[T]): 实体列表
        """
        # 将实体转换为字典
        rows = [entity.to_dict() for entity in entities]
        
        if not rows:
            # 如果没有实体，创建空文件
            with open(self.data_file, 'w', newline='', encoding='utf-8') as f:
                pass
            return
        
        # 获取所有字段
        fieldnames = rows[0].keys()
        
        # 写入CSV文件
        with open(self.data_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows) 