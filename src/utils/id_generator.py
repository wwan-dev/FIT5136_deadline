#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ID生成器工具类，用于为实体生成唯一标识符
"""

import os
import csv
from typing import Dict, Optional

class IdGenerator:
    """ID生成器工具类，用于为实体生成唯一标识符"""
    
    # 存储各实体类型的最大ID值
    __max_ids: Dict[str, int] = {}
    
    @classmethod
    def initialize(cls, data_dir: str = "data") -> None:
        """初始化ID生成器，获取各类型实体的最大ID
        
        Args:
            data_dir (str, optional): 数据目录. 默认为 "data".
        """
        # 确保数据目录存在
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # 初始化最大ID字典
        cls.__max_ids = {}
        
        # 查找数据目录下的所有CSV文件
        for filename in os.listdir(data_dir):
            if filename.endswith(".csv"):
                entity_type = filename.replace(".csv", "")
                file_path = os.path.join(data_dir, filename)
                
                # 初始化最大ID为0
                max_id = 0
                
                # 读取CSV文件获取最大ID
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
                
                # 保存最大ID值
                cls.__max_ids[entity_type] = max_id
    
    @classmethod
    def next_id(cls, entity_type: str) -> int:
        """获取指定实体类型的下一个可用ID
        
        Args:
            entity_type (str): 实体类型名称（如"users", "clinics", "doctors", "doctor_schedules", "appointments", "notifications"）
            
        Returns:
            int: 下一个可用的ID
            
        Raises:
            ValueError: 如果未初始化ID生成器
        """
        # 如果没有初始化，先初始化
        if not cls.__max_ids:
            cls.initialize()
        
        # 获取当前实体类型的最大ID
        max_id = cls.__max_ids.get(entity_type, 0)
        
        # 生成下一个ID
        next_id = max_id + 1
        
        # 更新最大ID记录
        cls.__max_ids[entity_type] = next_id
        
        return next_id
    
    @classmethod
    def get_max_id(cls, entity_type: str) -> int:
        """获取指定实体类型的当前最大ID
        
        Args:
            entity_type (str): 实体类型名称
            
        Returns:
            int: 当前最大ID，如果实体类型不存在则返回0
        """
        # 如果没有初始化，先初始化
        if not cls.__max_ids:
            cls.initialize()
            
        return cls.__max_ids.get(entity_type, 0) 