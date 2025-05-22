#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用户仓库类
"""

import os
from typing import List, Optional
from src.entities.user import User
from src.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    """用户仓库类"""
    
    def __init__(self):
        """初始化用户仓库"""
        data_file = os.path.join("data", "users.csv")
        super().__init__(data_file, User)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """根据电子邮箱获取用户
        
        Args:
            email (str): 用户电子邮箱
            
        Returns:
            Optional[User]: 用户，如果不存在则返回None
        """
        users = self.get_all()
        
        for user in users:
            if user.email == email:
                return user
        
        return None
    
    def get_patients(self) -> List[User]:
        """获取所有患者
        
        Returns:
            List[User]: 患者列表
        """
        users = self.get_all()
        return [user for user in users if user.is_patient()]
    
    def get_admins(self) -> List[User]:
        """获取所有管理员
        
        Returns:
            List[User]: 管理员列表
        """
        users = self.get_all()
        return [user for user in users if user.is_admin()]
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """验证用户登录
        
        Args:
            email (str): 用户电子邮箱
            password (str): 用户密码
            
        Returns:
            Optional[User]: 用户，如果验证失败则返回None
        """
        user = self.get_by_email(email)
        
        if user and user.password == password:
            return user
        
        return None

    # ─────────────────────────────────────────────
    # 新增：保存更新后的用户信息到 users.csv
    # ─────────────────────────────────────────────
    def update_user(self, user: User) -> bool:
        """
        用 user.id 作为主键，将该用户整行写回 users.csv
        """
        from src.utils.file_util import FileUtil

        # 读取当前CSV文件以获取可用的字段名
        existing_data = FileUtil.read_csv(self.data_file)
        if not existing_data:
            return False
        
        # 获取当前CSV文件的字段名
        available_fields = existing_data[0].keys()
        
        # 只保留CSV文件中存在的字段
        user_dict = user.to_dict()
        update_data = {k: v for k, v in user_dict.items() if k in available_fields}
        
        return FileUtil.update_row(
            self.data_file,
            lambda row: row.get("id") == str(user.id),
            update_data
        )
