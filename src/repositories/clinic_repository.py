#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
诊所仓库类
"""

import os
from typing import List, Optional
from src.entities.clinic import Clinic
from src.repositories.base_repository import BaseRepository

class ClinicRepository(BaseRepository[Clinic]):
    """诊所仓库类"""
    
    def __init__(self):
        """初始化诊所仓库"""
        data_file = os.path.join("data", "clinics.csv")
        super().__init__(data_file, Clinic)
    
    def get_by_suburb(self, suburb: str) -> List[Clinic]:
        """根据郊区获取诊所列表
        
        Args:
            suburb (str): 郊区
            
        Returns:
            List[Clinic]: 诊所列表
        """
        clinics = self.get_all()
        return [clinic for clinic in clinics if clinic.suburb.lower() == suburb.lower()]
    
    def get_by_name(self, name: str) -> Optional[Clinic]:
        """根据名称获取诊所
        
        Args:
            name (str): 诊所名称
            
        Returns:
            Optional[Clinic]: 诊所，如果不存在则返回None
        """
        clinics = self.get_all()
        
        for clinic in clinics:
            if clinic.name.lower() == name.lower():
                return clinic
        
        return None
    
    def search(self, keyword: str) -> List[Clinic]:
        """搜索诊所
        
        Args:
            keyword (str): 关键字
            
        Returns:
            List[Clinic]: 诊所列表
        """
        clinics = self.get_all()
        keyword = keyword.lower()
        
        return [clinic for clinic in clinics if 
                keyword in clinic.name.lower() or 
                keyword in clinic.suburb.lower() or 
                keyword in clinic.address.lower()] 