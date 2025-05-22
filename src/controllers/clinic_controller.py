#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
诊所和医生管理控制器类 - 处理诊所和医生的管理功能
"""

import os
from typing import Optional, Dict, Any, List

from src.entities.user import User
from src.entities.clinic import Clinic
from src.entities.doctor import Doctor
from src.repositories.clinic_repository import ClinicRepository
from src.repositories.doctor_repository import DoctorRepository

class ClinicController:
    """诊所和医生管理控制器类"""
    
    def __init__(self, user=None):
        """初始化诊所和医生管理控制器
        
        Args:
            user (User, optional): 当前用户. Defaults to None.
        """
        self.__clinic_repo = ClinicRepository()
        self.__doctor_repo = DoctorRepository()
        self.__current_user = user
        self.__should_return_to_main = False  # 是否返回主菜单标志
    
    def clear_screen(self):
        """清屏"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """打印标题"""
        self.clear_screen()
        print("=" * 50)
        print(f"{title.center(48)}")
        print()
    
    def wait_for_key(self):
        """等待用户按键"""
        input("\n按回车键继续...")
    
    # ================ 诊所管理功能 ================
    def show_all_clinics(self) -> None:
        """显示所有诊所"""
        self.print_header("所有诊所")
        
        clinics = self.__clinic_repo.get_all()
        
        if not clinics:
            print("系统中没有诊所记录")
            self.wait_for_key()
            return
        
        print(f"{'ID':<5}{'名称':<15}{'区域':<10}{'地址':<25}{'电话':<15}")
        print("-" * 70)
        
        for clinic in clinics:
            print(f"{clinic.id:<5}{clinic.name:<15}{clinic.suburb:<10}{clinic.address:<25}{clinic.phone:<15}")
        
        print("\n请选择操作:")
        print("1. 添加新诊所")
        print("2. 编辑诊所")
        print("3. 删除诊所")
        print("0. 返回上一级")
        print("-. 返回主菜单")
        
        choice = input("\n请选择: ").strip()
        
        if choice == "-":
            self.__should_return_to_main = True
            return
            
        if choice == "0":
            return
            
        if choice == "1":
            self.add_clinic()
        elif choice == "2":
            self.edit_clinic()
        elif choice == "3":
            self.delete_clinic()
        else:
            print("无效选项")
            self.wait_for_key()
    
    def add_clinic(self) -> None:
        """添加新诊所"""
        self.print_header("添加新诊所")
        
        name = input("诊所名称: ").strip()
        if not name:
            print("名称不能为空")
            self.wait_for_key()
            return
        
        # 检查诊所名称是否已存在
        existing_clinic = self.__clinic_repo.get_by_name(name)
        if existing_clinic:
            print(f"诊所 '{name}' 已存在")
            self.wait_for_key()
            return
        
        suburb = input("所在区域: ").strip()
        address = input("详细地址: ").strip()
        phone = input("联系电话: ").strip()
        
        # 创建新诊所
        new_clinic = Clinic(
            name=name,
            suburb=suburb,
            address=address,
            phone=phone
        )
        
        # 保存诊所
        try:
            saved_clinic = self.__clinic_repo.add(new_clinic)
            print(f"\n成功添加诊所: {saved_clinic.name} (ID: {saved_clinic.id})")
        except Exception as e:
            print(f"添加诊所失败: {str(e)}")
        
        self.wait_for_key()
    
    def edit_clinic(self) -> None:
        """编辑诊所信息"""
        self.print_header("编辑诊所")
        
        clinic_id = input("请输入要编辑的诊所ID (0返回): ").strip()
        
        if clinic_id == "0":
            return
        
        try:
            clinic_id = int(clinic_id)
            clinic = self.__clinic_repo.get_by_id(clinic_id)
            
            if not clinic:
                print(f"找不到ID为 {clinic_id} 的诊所")
                self.wait_for_key()
                return
                
            print(f"\n当前诊所信息:")
            print(f"ID: {clinic.id}")
            print(f"名称: {clinic.name}")
            print(f"区域: {clinic.suburb}")
            print(f"地址: {clinic.address}")
            print(f"电话: {clinic.phone}")
            
            print("\n请选择要编辑的字段:")
            print("1. 名称")
            print("2. 区域")
            print("3. 地址")
            print("4. 电话")
            print("0. 返回")
            
            field = input("\n请选择: ").strip()
            
            if field == "0":
                return
                
            if field == "1":
                new_name = input(f"新名称 (当前: {clinic.name}): ").strip()
                if new_name:
                    clinic.name = new_name
            elif field == "2":
                new_suburb = input(f"新区域 (当前: {clinic.suburb}): ").strip()
                if new_suburb:
                    clinic.suburb = new_suburb
            elif field == "3":
                new_address = input(f"新地址 (当前: {clinic.address}): ").strip()
                if new_address:
                    clinic.address = new_address
            elif field == "4":
                new_phone = input(f"新电话 (当前: {clinic.phone}): ").strip()
                if new_phone:
                    clinic.phone = new_phone
            else:
                print("无效选项")
                self.wait_for_key()
                return
            
            # 更新诊所
            try:
                self.__clinic_repo.update(clinic)
                print("\n诊所信息已更新")
            except Exception as e:
                print(f"更新诊所失败: {str(e)}")
            
        except ValueError:
            print("无效的诊所ID")
        
        self.wait_for_key()
    
    def delete_clinic(self) -> None:
        """删除诊所"""
        self.print_header("删除诊所")
        
        clinic_id = input("请输入要删除的诊所ID (0返回): ").strip()
        
        if clinic_id == "0":
            return
        
        try:
            clinic_id = int(clinic_id)
            clinic = self.__clinic_repo.get_by_id(clinic_id)
            
            if not clinic:
                print(f"找不到ID为 {clinic_id} 的诊所")
                self.wait_for_key()
                return
                
            # 检查是否有医生关联到该诊所
            doctors = self.__doctor_repo.get_by_clinic(clinic_id)
            if doctors:
                print(f"无法删除诊所，有 {len(doctors)} 名医生关联到该诊所")
                print("请先将这些医生从该诊所移除")
                self.wait_for_key()
                return
            
            print(f"\n即将删除诊所: {clinic.name} (ID: {clinic.id})")
            confirm = input("确认删除? (Y/N): ").strip().upper()
            
            if confirm == "Y":
                try:
                    self.__clinic_repo.delete(clinic.id)
                    print("\n诊所已删除")
                except Exception as e:
                    print(f"删除诊所失败: {str(e)}")
            else:
                print("已取消删除")
            
        except ValueError:
            print("无效的诊所ID")
        
        self.wait_for_key()
    
    def search_clinics(self) -> None:
        """搜索诊所"""
        self.print_header("搜索诊所")
        
        keyword = input("请输入搜索关键词 (0返回): ").strip()
        
        if keyword == "0":
            return
        
        if not keyword:
            print("搜索关键词不能为空")
            self.wait_for_key()
            return
        
        clinics = self.__clinic_repo.search(keyword)
        
        if not clinics:
            print(f"没有找到匹配 '{keyword}' 的诊所")
            self.wait_for_key()
            return
        
        print(f"\n找到 {len(clinics)} 个匹配的诊所:")
        print(f"{'ID':<5}{'名称':<15}{'区域':<10}{'地址':<25}{'电话':<15}")
        print("-" * 70)
        
        for clinic in clinics:
            print(f"{clinic.id:<5}{clinic.name:<15}{clinic.suburb:<10}{clinic.address:<25}{clinic.phone:<15}")
        
        self.wait_for_key()
    
    # ================ 医生管理功能 ================
    def show_all_doctors(self) -> None:
        """显示所有医生"""
        self.print_header("所有医生")
        
        doctors = self.__doctor_repo.get_all()
        
        if not doctors:
            print("系统中没有医生记录")
            self.wait_for_key()
            return
        
        print(f"{'ID':<5}{'姓名':<15}{'电子邮箱':<25}{'专业':<25}")
        print("-" * 70)
        
        for doctor in doctors:
            specialisations = ", ".join(doctor.specialisation)
            print(f"{doctor.id:<5}{doctor.full_name:<15}{doctor.email:<25}{specialisations:<25}")
        
        print("\n请选择操作:")
        print("1. 添加新医生")
        print("2. 编辑医生")
        print("3. 删除医生")
        print("4. 管理医生诊所关联")
        print("0. 返回上一级")
        print("-. 返回主菜单")
        
        choice = input("\n请选择: ").strip()
        
        if choice == "-":
            self.__should_return_to_main = True
            return
            
        if choice == "0":
            return
            
        if choice == "1":
            self.add_doctor()
        elif choice == "2":
            self.edit_doctor()
        elif choice == "3":
            self.delete_doctor()
        elif choice == "4":
            self.manage_doctor_clinics()
        else:
            print("无效选项")
            self.wait_for_key()
    
    def add_doctor(self) -> None:
        """添加新医生"""
        self.print_header("添加新医生")
        
        full_name = input("医生姓名: ").strip()
        if not full_name:
            print("姓名不能为空")
            self.wait_for_key()
            return
        
        email = input("电子邮箱: ").strip()
        if not email:
            print("电子邮箱不能为空")
            self.wait_for_key()
            return
        
        # 检查电子邮箱是否已存在
        existing_doctor = self.__doctor_repo.get_by_email(email)
        if existing_doctor:
            print(f"电子邮箱 '{email}' 已被使用")
            self.wait_for_key()
            return
        
        # 专业领域
        specialisations = []
        while True:
            spec = input("专业领域 (回车结束添加): ").strip()
            if not spec:
                break
            specialisations.append(spec)
        
        # 创建新医生
        new_doctor = Doctor(
            full_name=full_name,
            email=email,
            specialisation=specialisations
        )
        
        # 保存医生
        try:
            saved_doctor = self.__doctor_repo.add(new_doctor)
            print(f"\n成功添加医生: {saved_doctor.full_name} (ID: {saved_doctor.id})")
        except Exception as e:
            print(f"添加医生失败: {str(e)}")
        
        self.wait_for_key()
    
    def edit_doctor(self) -> None:
        """编辑医生信息"""
        self.print_header("编辑医生")
        
        doctor_id = input("请输入要编辑的医生ID (0返回): ").strip()
        
        if doctor_id == "0":
            return
        
        try:
            doctor_id = int(doctor_id)
            doctor = self.__doctor_repo.get_by_id(doctor_id)
            
            if not doctor:
                print(f"找不到ID为 {doctor_id} 的医生")
                self.wait_for_key()
                return
                
            print(f"\n当前医生信息:")
            print(f"ID: {doctor.id}")
            print(f"姓名: {doctor.full_name}")
            print(f"电子邮箱: {doctor.email}")
            print(f"专业领域: {', '.join(doctor.specialisation)}")
            
            print("\n请选择要编辑的字段:")
            print("1. 姓名")
            print("2. 电子邮箱")
            print("3. 管理专业领域")
            print("0. 返回")
            
            field = input("\n请选择: ").strip()
            
            if field == "0":
                return
                
            if field == "1":
                new_name = input(f"新姓名 (当前: {doctor.full_name}): ").strip()
                if new_name:
                    doctor.full_name = new_name
            elif field == "2":
                new_email = input(f"新电子邮箱 (当前: {doctor.email}): ").strip()
                if new_email:
                    doctor.email = new_email
            elif field == "3":
                self.manage_doctor_specialisations(doctor)
                return
            else:
                print("无效选项")
                self.wait_for_key()
                return
            
            # 更新医生
            try:
                self.__doctor_repo.update(doctor)
                print("\n医生信息已更新")
            except Exception as e:
                print(f"更新医生失败: {str(e)}")
            
        except ValueError:
            print("无效的医生ID")
        
        self.wait_for_key()
    
    def manage_doctor_specialisations(self, doctor: Doctor) -> None:
        """管理医生专业领域"""
        while True:
            self.print_header(f"管理医生 {doctor.full_name} 的专业领域")
            
            print("当前专业领域:")
            if doctor.specialisation:
                for i, spec in enumerate(doctor.specialisation, 1):
                    print(f"{i}. {spec}")
            else:
                print("(无)")
            
            print("\n请选择操作:")
            print("1. 添加专业领域")
            print("2. 删除专业领域")
            print("0. 返回")
            
            choice = input("\n请选择: ").strip()
            
            if choice == "0":
                return
                
            if choice == "1":
                new_spec = input("新专业领域: ").strip()
                if new_spec:
                    doctor.add_specialisation(new_spec)
                    try:
                        self.__doctor_repo.update(doctor)
                        print(f"已添加专业领域: {new_spec}")
                    except Exception as e:
                        print(f"更新失败: {str(e)}")
                    self.wait_for_key()
            elif choice == "2":
                if not doctor.specialisation:
                    print("没有可删除的专业领域")
                    self.wait_for_key()
                    continue
                
                try:
                    index = int(input("请输入要删除的专业领域编号: ").strip()) - 1
                    if 0 <= index < len(doctor.specialisation):
                        spec_to_remove = doctor.specialisation[index]
                        doctor.remove_specialisation(spec_to_remove)
                        try:
                            self.__doctor_repo.update(doctor)
                            print(f"已删除专业领域: {spec_to_remove}")
                        except Exception as e:
                            print(f"更新失败: {str(e)}")
                    else:
                        print("无效的编号")
                except ValueError:
                    print("请输入有效的数字")
                self.wait_for_key()
            else:
                print("无效选项")
                self.wait_for_key()
    
    def delete_doctor(self) -> None:
        """删除医生"""
        self.print_header("删除医生")
        
        doctor_id = input("请输入要删除的医生ID (0返回): ").strip()
        
        if doctor_id == "0":
            return
        
        try:
            doctor_id = int(doctor_id)
            doctor = self.__doctor_repo.get_by_id(doctor_id)
            
            if not doctor:
                print(f"找不到ID为 {doctor_id} 的医生")
                self.wait_for_key()
                return
            
            print(f"\n即将删除医生: {doctor.full_name} (ID: {doctor.id})")
            confirm = input("确认删除? (Y/N): ").strip().upper()
            
            if confirm == "Y":
                try:
                    self.__doctor_repo.delete(doctor.id)
                    print("\n医生已删除")
                except Exception as e:
                    print(f"删除医生失败: {str(e)}")
            else:
                print("已取消删除")
            
        except ValueError:
            print("无效的医生ID")
        
        self.wait_for_key()
    
    def manage_doctor_clinics(self) -> None:
        """管理医生与诊所的关联"""
        self.print_header("管理医生诊所关联")
        
        doctor_id = input("请输入医生ID (0返回): ").strip()
        
        if doctor_id == "0":
            return
        
        try:
            doctor_id = int(doctor_id)
            doctor = self.__doctor_repo.get_by_id(doctor_id)
            
            if not doctor:
                print(f"找不到ID为 {doctor_id} 的医生")
                self.wait_for_key()
                return
            
            while True:
                self.print_header(f"管理医生 {doctor.full_name} 的诊所关联")
                
                # 显示当前关联的诊所
                print("当前关联的诊所:")
                if doctor.assigned_clinics:
                    for clinic_id in doctor.assigned_clinics:
                        clinic = self.__clinic_repo.get_by_id(clinic_id)
                        if clinic:
                            print(f"ID: {clinic.id}, 名称: {clinic.name}, 区域: {clinic.suburb}")
                else:
                    print("(无)")
                
                print("\n请选择操作:")
                print("1. 添加诊所关联")
                print("2. 移除诊所关联")
                print("0. 返回")
                
                choice = input("\n请选择: ").strip()
                
                if choice == "0":
                    return
                    
                if choice == "1":
                    self.add_clinic_to_doctor(doctor)
                elif choice == "2":
                    self.remove_clinic_from_doctor(doctor)
                else:
                    print("无效选项")
                    self.wait_for_key()
            
        except ValueError:
            print("无效的医生ID")
            self.wait_for_key()
    
    def add_clinic_to_doctor(self, doctor: Doctor) -> None:
        """为医生添加诊所关联"""
        self.print_header(f"为医生 {doctor.full_name} 添加诊所")
        
        # 显示所有诊所
        clinics = self.__clinic_repo.get_all()
        
        if not clinics:
            print("系统中没有诊所记录")
            self.wait_for_key()
            return
        
        print("可用诊所:")
        available_clinics = []
        for clinic in clinics:
            if clinic.id not in doctor.assigned_clinics:
                available_clinics.append(clinic)
                print(f"ID: {clinic.id}, 名称: {clinic.name}, 区域: {clinic.suburb}")
        
        if not available_clinics:
            print("没有可添加的诊所")
            self.wait_for_key()
            return
        
        try:
            clinic_id = int(input("\n请输入要添加的诊所ID (0返回): ").strip())
            
            if clinic_id == 0:
                return
            
            # 检查诊所ID是否有效
            clinic = self.__clinic_repo.get_by_id(clinic_id)
            if not clinic:
                print(f"找不到ID为 {clinic_id} 的诊所")
                self.wait_for_key()
                return
            
            # 检查是否已关联
            if clinic.id in doctor.assigned_clinics:
                print(f"医生已关联到诊所 {clinic.name}")
                self.wait_for_key()
                return
            
            # 添加关联
            doctor.add_clinic(clinic.id)
            
            # 更新医生
            try:
                self.__doctor_repo.update(doctor)
                print(f"\n已将医生 {doctor.full_name} 关联到诊所 {clinic.name}")
            except Exception as e:
                print(f"更新失败: {str(e)}")
            
        except ValueError:
            print("无效的诊所ID")
        
        self.wait_for_key()
    
    def remove_clinic_from_doctor(self, doctor: Doctor) -> None:
        """移除医生的诊所关联"""
        self.print_header(f"移除医生 {doctor.full_name} 的诊所关联")
        
        if not doctor.assigned_clinics:
            print("医生没有关联的诊所")
            self.wait_for_key()
            return
        
        print("当前关联的诊所:")
        for clinic_id in doctor.assigned_clinics:
            clinic = self.__clinic_repo.get_by_id(clinic_id)
            if clinic:
                print(f"ID: {clinic.id}, 名称: {clinic.name}, 区域: {clinic.suburb}")
        
        try:
            clinic_id = int(input("\n请输入要移除的诊所ID (0返回): ").strip())
            
            if clinic_id == 0:
                return
            
            # 检查诊所ID是否已关联
            if clinic_id not in doctor.assigned_clinics:
                print(f"医生未关联到ID为 {clinic_id} 的诊所")
                self.wait_for_key()
                return
            
            # 获取诊所名称
            clinic = self.__clinic_repo.get_by_id(clinic_id)
            clinic_name = clinic.name if clinic else f"ID {clinic_id}"
            
            # 移除关联
            doctor.remove_clinic(clinic_id)
            
            # 更新医生
            try:
                self.__doctor_repo.update(doctor)
                print(f"\n已移除医生 {doctor.full_name} 与诊所 {clinic_name} 的关联")
            except Exception as e:
                print(f"更新失败: {str(e)}")
            
        except ValueError:
            print("无效的诊所ID")
        
        self.wait_for_key()
    
    def search_doctors(self) -> None:
        """搜索医生"""
        self.print_header("搜索医生")
        
        keyword = input("请输入搜索关键词 (0返回): ").strip()
        
        if keyword == "0":
            return
        
        if not keyword:
            print("搜索关键词不能为空")
            self.wait_for_key()
            return
        
        doctors = self.__doctor_repo.search(keyword)
        
        if not doctors:
            print(f"没有找到匹配 '{keyword}' 的医生")
            self.wait_for_key()
            return
        
        print(f"\n找到 {len(doctors)} 个匹配的医生:")
        print(f"{'ID':<5}{'姓名':<15}{'电子邮箱':<25}{'专业':<25}")
        print("-" * 70)
        
        for doctor in doctors:
            specialisations = ", ".join(doctor.specialisation)
            print(f"{doctor.id:<5}{doctor.full_name:<15}{doctor.email:<25}{specialisations:<25}")
        
        self.wait_for_key()
    
    # ================ 主菜单 ================
    def run(self) -> None:
        """运行诊所和医生管理菜单"""
        self.__should_return_to_main = False  # 重置返回主菜单标志
        
        while True:
            if self.__should_return_to_main:
                break
                
            self.print_header("诊所和医生管理")
            
            print("1. 查看所有诊所")
            print("2. 搜索诊所")
            print("3. 查看所有医生")
            print("4. 搜索医生")
            print("0. 返回上一级")
            print("-. 返回主菜单")
            
            choice = input("\n请选择操作: ").strip()
            
            if choice == "1":
                self.show_all_clinics()
            elif choice == "2":
                self.search_clinics()
            elif choice == "3":
                self.show_all_doctors()
            elif choice == "4":
                self.search_doctors()
            elif choice == "0":
                break
            elif choice == "-":
                self.__should_return_to_main = True
                break
            else:
                print("无效选项")
                self.wait_for_key()
        
        return self.__should_return_to_main  # 返回标志，供调用者判断是否返回主菜单 