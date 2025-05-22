#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
基础仓库类
"""

import os
from typing import List, Dict, Any, TypeVar, Generic, Type, Optional
from src.utils.file_util import FileUtil

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
        FileUtil.ensure_file_exists(data_file)
    
    def get_all(self) -> List[T]:
        """获取所有实体
        
        Returns:
            List[T]: 实体列表
        """
        entities = []
        
        # 读取CSV文件
        rows = FileUtil.read_csv(self.data_file)
        
        # 转换为实体对象
        for row in rows:
            entity = self.entity_class.from_dict(row)
            entities.append(entity)
        
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
        # 如果是新实体，生成ID
        if entity.id is None:
            entity.id = FileUtil.get_next_id(self.data_file)
        
        # 将实体转换为字典
        entity_dict = entity.to_dict()
        
        # 追加到CSV文件
        FileUtil.append_csv(self.data_file, entity_dict)
        
        return entity
    
    def update(self, entity: T) -> T:
        """更新实体
        
        Args:
            entity (T): 要更新的实体
            
        Returns:
            T: 更新后的实体
        """
        # 将实体转换为字典
        entity_dict = entity.to_dict()
        
        # 更新CSV文件中的行
        FileUtil.update_row(
            self.data_file,
            lambda row: str(row.get('id')) == str(entity.id),
            entity_dict
        )
        
        return entity
    
    def delete(self, entity_id) -> bool:
        """删除实体
        
        Args:
            entity_id: 实体ID
            
        Returns:
            bool: 是否删除成功
        """
        # 从CSV文件中删除行
        return FileUtil.delete_row(
            self.data_file,
            lambda row: str(row.get('id')) == str(entity_id)
        )
    
    def _save_all(self, entities: List[T]) -> None:
        """保存所有实体到文件
        
        Args:
            entities (List[T]): 实体列表
        """
        # 将实体转换为字典
        rows = [entity.to_dict() for entity in entities]
        
        # 写入CSV文件
        FileUtil.write_csv(self.data_file, rows) 