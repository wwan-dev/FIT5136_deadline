#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
文件工具类，提供对CSV文件的读写功能
"""

import os
import csv
from typing import List, Dict, Any, Optional

class FileUtil:
    """文件工具类，提供对CSV文件的读写功能"""
    
    @staticmethod
    def ensure_file_exists(file_path: str) -> None:
        """确保文件存在，如果不存在则创建空文件
        
        Args:
            file_path (str): 文件路径
        """
        if not os.path.exists(file_path):
            # 创建目录
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # 创建空文件
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                pass
    
    @staticmethod
    def read_csv(file_path: str) -> List[Dict[str, Any]]:
        """读取CSV文件
        
        Args:
            file_path (str): 文件路径
            
        Returns:
            List[Dict[str, Any]]: 数据列表，每个元素是一个字典
        """
        FileUtil.ensure_file_exists(file_path)
        
        data = []
        try:
            with open(file_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames:  # 确保文件不为空
                    for row in reader:
                        # 处理空值
                        processed_row = {}
                        for key, value in row.items():
                            if value == '':
                                processed_row[key] = None
                            else:
                                processed_row[key] = value
                        data.append(processed_row)
        except Exception as e:
            print(f"读取文件 {file_path} 时出错: {e}")
            
        return data
    
    @staticmethod
    def write_csv(file_path: str, data: List[Dict[str, Any]]) -> bool:
        """写入CSV文件
        
        Args:
            file_path (str): 文件路径
            data (List[Dict[str, Any]]): 数据列表，每个元素是一个字典
            
        Returns:
            bool: 是否写入成功
        """
        FileUtil.ensure_file_exists(file_path)
        
        if not data:
            # 如果没有数据，创建空文件
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                pass
            return True
        
        try:
            # 获取所有字段
            fieldnames = data[0].keys()
            
            # 写入CSV文件
            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            
            return True
        except Exception as e:
            print(f"写入文件 {file_path} 时出错: {e}")
            return False
    
    @staticmethod
    def append_csv(file_path: str, row: Dict[str, Any]) -> bool:
        """追加一行数据到CSV文件
        
        Args:
            file_path (str): 文件路径
            row (Dict[str, Any]): 要追加的数据行
            
        Returns:
            bool: 是否追加成功
        """
        FileUtil.ensure_file_exists(file_path)
        
        try:
            # 读取现有数据
            existing_data = FileUtil.read_csv(file_path)
            
            if not existing_data:
                # 如果文件为空，直接写入
                return FileUtil.write_csv(file_path, [row])
            
            # 确保字段一致
            for key in row.keys():
                if key not in existing_data[0]:
                    existing_data[0][key] = None
            
            for key in existing_data[0].keys():
                if key not in row:
                    row[key] = None
            
            # 追加数据
            existing_data.append(row)
            
            # 写回文件
            return FileUtil.write_csv(file_path, existing_data)
        except Exception as e:
            print(f"追加数据到文件 {file_path} 时出错: {e}")
            return False
    
    @staticmethod
    def delete_row(file_path: str, condition: callable) -> bool:
        """从CSV文件中删除符合条件的行
        
        Args:
            file_path (str): 文件路径
            condition (callable): 条件函数，接受一个字典参数，返回布尔值
            
        Returns:
            bool: 是否删除成功
        """
        FileUtil.ensure_file_exists(file_path)
        
        try:
            # 读取现有数据
            existing_data = FileUtil.read_csv(file_path)
            
            if not existing_data:
                return True
            
            # 过滤数据
            filtered_data = [row for row in existing_data if not condition(row)]
            
            # 如果没有行被删除，直接返回
            if len(filtered_data) == len(existing_data):
                return True
            
            # 写回文件
            return FileUtil.write_csv(file_path, filtered_data)
        except Exception as e:
            print(f"从文件 {file_path} 删除数据时出错: {e}")
            return False
    
    @staticmethod
    def update_row(file_path: str, condition: callable, update_data: Dict[str, Any]) -> bool:
        """更新CSV文件中符合条件的行
        
        Args:
            file_path (str): 文件路径
            condition (callable): 条件函数，接受一个字典参数，返回布尔值
            update_data (Dict[str, Any]): 要更新的数据
            
        Returns:
            bool: 是否更新成功
        """
        FileUtil.ensure_file_exists(file_path)
        
        try:
            # 读取现有数据
            existing_data = FileUtil.read_csv(file_path)
            
            if not existing_data:
                return True
            
            # 更新数据
            for row in existing_data:
                if condition(row):
                    for key, value in update_data.items():
                        row[key] = value
            
            # 写回文件
            return FileUtil.write_csv(file_path, existing_data)
        except Exception as e:
            print(f"更新文件 {file_path} 中的数据时出错: {e}")
            return False
    
    @staticmethod
    def get_next_id(file_path: str, id_field: str = 'id') -> int:
        """获取下一个可用的ID
        
        Args:
            file_path (str): 文件路径
            id_field (str, optional): ID字段名. 默认为 'id'.
            
        Returns:
            int: 下一个可用的ID
        """
        FileUtil.ensure_file_exists(file_path)
        
        try:
            # 读取现有数据
            existing_data = FileUtil.read_csv(file_path)
            
            if not existing_data:
                return 1
            
            # 找出最大ID
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
            print(f"获取文件 {file_path} 中的下一个ID时出错: {e}")
            return 1 
