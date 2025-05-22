#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
医生仓库类
"""

import os
from typing import List, Optional
from src.entities.doctor import Doctor
from src.repositories.base_repository import BaseRepository

class DoctorRepository(BaseRepository[Doctor]):
    """医生仓库类"""
    
    def __init__(self):
        """初始化医生仓库"""
        data_file = os.path.join("data", "doctors.csv")
        super().__init__(data_file, Doctor)
    
    def get_by_clinic(self, clinic_id: int) -> List[Doctor]:
        """根据诊所ID获取医生列表
        
        Args:
            clinic_id (int): 诊所ID
            
        Returns:
            List[Doctor]: 医生列表
        """
        doctors = self.get_all()
        return [doctor for doctor in doctors if doctor.is_working_in_clinic(clinic_id)]
    
    def get_by_specialisation(self, specialisation: str) -> List[Doctor]:
        """根据专业领域获取医生列表
        
        Args:
            specialisation (str): 专业领域
            
        Returns:
            List[Doctor]: 医生列表
        """
        doctors = self.get_all()
        return [doctor for doctor in doctors if doctor.has_specialisation(specialisation)]
    
    def get_by_email(self, email: str) -> Optional[Doctor]:
        """根据电子邮箱获取医生
        
        Args:
            email (str): 医生电子邮箱
            
        Returns:
            Optional[Doctor]: 医生，如果不存在则返回None
        """
        doctors = self.get_all()
        
        for doctor in doctors:
            if doctor.email == email:
                return doctor
        
        return None
    
    def search(self, keyword: str) -> List[Doctor]:
        """搜索医生
        
        Args:
            keyword (str): 关键字
            
        Returns:
            List[Doctor]: 医生列表
        """
        doctors = self.get_all()
        keyword = keyword.lower()
        
        result = []
        for doctor in doctors:
            if keyword in doctor.full_name.lower() or keyword in doctor.email.lower():
                result.append(doctor)
                continue
            
            # 检查专业领域
            for spec in doctor.specialisation:
                if keyword in spec.lower():
                    result.append(doctor)
                    break
        
        return result 
