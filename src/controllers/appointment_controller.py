#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
预约控制器类
"""

import os
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any

from src.entities.user import User
from src.entities.appointment import Appointment
from src.entities.notification import Notification
from src.repositories.appointment_repository import AppointmentRepository
from src.repositories.clinic_repository import ClinicRepository
from src.repositories.doctor_repository import DoctorRepository
from src.repositories.notification_repository import NotificationRepository
from src.repositories.doctor_schedule_repository import DoctorScheduleRepository
from src.repositories.user_repository import UserRepository
from src.utils.date_util import DateUtil


class AppointmentController:
    """预约控制器类"""
    
    def __init__(self, user=None):
        """初始化预约控制器
        
        Args:
            user (User, optional): 当前用户. Defaults to None.
        """
        self.__appointment_repo = AppointmentRepository()
        self.__clinic_repo = ClinicRepository()
        self.__doctor_repo = DoctorRepository()
        self.__schedule_repo = DoctorScheduleRepository()
        self.__notification_repo = NotificationRepository()
        self.__current_user = user
    
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
    
    def get_clinic_selection(self, default_option: bool = True) -> Optional[int]:
        """显示诊所选择界面
        
        Args:
            default_option (bool): 是否显示默认选项（所有诊所）
            
        Returns:
            Optional[int]: 选择的诊所ID，如果选择所有诊所则返回None
        """
        self.print_header("选择诊所")
        
        clinics = self.__clinic_repo.get_all()
        
        if not clinics:
            print("没有找到诊所记录")
            self.wait_for_key()
            return None
        
        print(f"{'ID':<5}{'名称':<15}{'区域':<10}{'地址':<20}{'电话':<15}")
        print("-" * 65)
        
        for clinic in clinics:
            print(f"{clinic.id:<5}{clinic.name:<15}{clinic.suburb:<10}{clinic.address:<20}{clinic.phone:<15}")
        
        option_text = "\n请选择诊所ID"
        if default_option:
            option_text += "，或输入0查看所有诊所"
        option_text += "，或输入-1返回"
        option_text += "，直接按回车默认查看所有诊所: "
        
        print(option_text, end="")
        choice = input()
        
        if choice == "":
            return None  # 直接按回车默认查看所有诊所
        
        if choice == "-1":
            return -1
        
        if default_option and choice == "0":
            return None
        
        try:
            clinic_id = int(choice)
            selected_clinic = self.__clinic_repo.get_by_id(clinic_id)
            if selected_clinic:
                return clinic_id
            else:
                print("无效的诊所ID")
                self.wait_for_key()
                return self.get_clinic_selection(default_option)
        except ValueError:
            print("请输入有效的数字")
            self.wait_for_key()
            return self.get_clinic_selection(default_option)
    
    def get_doctor_selection(self, clinic_id: Optional[int] = None, default_option: bool = True) -> Optional[int]:
        """显示医生选择界面
        
        Args:
            clinic_id (Optional[int]): 诊所ID，如果指定则只显示该诊所的医生
            default_option (bool): 是否显示默认选项（所有医生）
            
        Returns:
            Optional[int]: 选择的医生ID，如果选择所有医生则返回None
        """
        self.print_header("选择医生")
        
        if clinic_id:
            doctors = self.__doctor_repo.get_by_clinic(clinic_id)
            print(f"诊所 {clinic_id} 的医生列表:")
        else:
            doctors = self.__doctor_repo.get_all()
            print("所有医生列表:")
        
        if not doctors:
            print("没有找到医生记录")
            self.wait_for_key()
            return None
        
        print(f"{'ID':<5}{'姓名':<15}{'电子邮箱':<25}{'专业':<20}")
        print("-" * 65)
        
        for doctor in doctors:
            specialisation = ", ".join(doctor.specialisation)
            print(f"{doctor.id:<5}{doctor.full_name:<15}{doctor.email:<25}{specialisation:<20}")
        
        option_text = "\n请选择医生ID"
        if default_option:
            option_text += "，或输入0查看所有医生"
        option_text += "，或输入-1返回"
        option_text += "，直接按回车默认查看所有医生: "
        
        print(option_text, end="")
        choice = input()
        
        if choice == "":
            return None  # 直接按回车默认查看所有医生
        
        if choice == "-1":
            return -1
        
        if default_option and choice == "0":
            return None
        
        try:
            doctor_id = int(choice)
            selected_doctor = self.__doctor_repo.get_by_id(doctor_id)
            if selected_doctor:
                return doctor_id
            else:
                print("无效的医生ID")
                self.wait_for_key()
                return self.get_doctor_selection(clinic_id, default_option)
        except ValueError:
            print("请输入有效的数字")
            self.wait_for_key()
            return self.get_doctor_selection(clinic_id, default_option)
    
    def get_date_selection(self, future_only: bool = True, default_option: bool = True) -> Optional[str]:
        """显示日期选择界面
        
        Args:
            future_only (bool): 是否只显示未来日期
            default_option (bool): 是否显示默认选项（所有日期）
            
        Returns:
            Optional[str]: 选择的日期，格式为YYYY-MM-DD，如果选择所有日期则返回None
        """
        self.print_header("选择日期")
        
        today = DateUtil.get_current_date()
        
        if future_only:
            # 获取未来7天的日期
            dates = DateUtil.get_date_range(today, 7)
            print("未来7天的日期:")
        else:
            # 获取过去7天和未来7天的日期
            past_dates = DateUtil.get_date_range(DateUtil.add_days(today, -7), 7)
            future_dates = DateUtil.get_date_range(today, 7)
            dates = past_dates + future_dates
            print("可选日期(过去7天和未来7天):")
        
        print(f"{'日期':<15}{'星期':<10}")
        print("-" * 25)
        
        for date in dates:
            day_of_week = DateUtil.get_day_of_week(date)
            print(f"{date:<15}{day_of_week:<10}")
        
        option_text = "\n请输入日期(YYYY-MM-DD)"
        if default_option:
            option_text += "，或输入0查看所有日期"
        option_text += "，或输入-1返回"
        option_text += f"，直接按回车默认选择今天({today}): "
        
        print(option_text, end="")
        choice = input()
        
        if choice == "":
            return today  # 直接按回车默认选择今天
        
        if choice == "-1":
            return -1
        
        if default_option and choice == "0":
            return None
        
        if not DateUtil.is_valid_date(choice):
            print("无效的日期格式，请使用YYYY-MM-DD格式")
            self.wait_for_key()
            return self.get_date_selection(future_only, default_option)
        
        if future_only and choice < today:
            print("请选择未来的日期")
            self.wait_for_key()
            return self.get_date_selection(future_only, default_option)
        
        return choice
    
    def get_available_time_slots(self, doctor_id: int, clinic_id: int, date: str) -> List[int]:
        """获取指定日期医生在诊所的可用时间槽
        
        Args:
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            date (str): 日期，格式为YYYY-MM-DD
            
        Returns:
            List[int]: 可用时间槽列表
        """
        # 获取医生在该诊所的排班
        doctor_schedule = self.__schedule_repo.get_by_doctor_clinic(doctor_id, clinic_id)
        
        # 如果没有找到排班，创建一个所有时间槽都可用的排班
        if not doctor_schedule:
            doctor_schedule = self.__schedule_repo.create_default_schedule(doctor_id, clinic_id)
        
        # 获取医生排班中可用时间槽
        available_slots_base = DateUtil.hex_to_time_slots(doctor_schedule.time_slots)
        
        # 如果医生没有可用时间槽，返回空列表
        if not available_slots_base:
            return []
        
        # 检查每个排班中的时间槽在该日期是否可用
        available_slots = []
        for slot in available_slots_base:
            if self.__appointment_repo.is_slot_available(doctor_id, clinic_id, date, slot):
                available_slots.append(slot)
        
        return available_slots
    
    def show_available_slots(self, params: Dict[str, Any] = None) -> Optional[Tuple[str, int, int, int]]:
        """显示可用的时间槽
        
        Args:
            params (Dict[str, Any], optional): 参数字典，可包含doctor_id, clinic_id, date
            
        Returns:
            Optional[Tuple[str, int, int, int]]: (日期, 时间槽, 医生ID, 诊所ID)元组，如果用户取消则返回None
        """
        params = params or {}
        
        # 获取参数
        clinic_id = params.get('clinic_id')
        doctor_id = params.get('doctor_id')
        date = params.get('date')
        
        # 如果未指定诊所，让用户选择
        if clinic_id is None:
            clinic_id = self.get_clinic_selection()
            if clinic_id == -1:  # 用户取消
                return None
        
        # 如果未指定医生，让用户选择
        if doctor_id is None:
            doctor_id = self.get_doctor_selection(clinic_id)
            if doctor_id == -1:  # 用户取消
                return None
        
        # 如果未指定日期，让用户选择
        if date is None:
            date = self.get_date_selection()
            if date == -1:  # 用户取消
                return None
        
        # 如果未指定任何筛选条件，需要用户至少选择一个
        if clinic_id is None and doctor_id is None and date is None:
            print("请至少选择一个筛选条件(诊所、医生或日期)")
            self.wait_for_key()
            return self.show_available_slots()
        
        self.print_header("可用时间槽")
        
        # 如果未指定日期，获取未来7天的日期
        if date is None:
            today = DateUtil.get_current_date()
            future_dates = DateUtil.get_date_range(today, 7)
        else:
            future_dates = [date]
        
        # 如果未指定诊所，获取所有诊所
        if clinic_id is None:
            clinics = self.__clinic_repo.get_all()
            clinic_ids = [clinic.id for clinic in clinics]
        else:
            clinic_ids = [clinic_id]
        
        # 如果未指定医生，获取所有医生
        if doctor_id is None:
            doctors = self.__doctor_repo.get_all()
            doctor_ids = [doctor.id for doctor in doctors]
        else:
            doctor_ids = [doctor_id]
        
        print("可用时间槽:")
        print(f"{'日期':<15}{'星期':<10}{'诊所':<15}{'医生':<15}{'可用时间'}")
        print("-" * 85)
        
        available_options = []
        option_index = 1
        
        # 遍历所有组合
        for d_id in doctor_ids:
            doctor = self.__doctor_repo.get_by_id(d_id)
            if not doctor:
                continue
                
            for c_id in clinic_ids:
                # 检查医生是否在该诊所工作
                if c_id not in doctor.assigned_clinics:
                    continue
                    
                clinic = self.__clinic_repo.get_by_id(c_id)
                if not clinic:
                    continue
                    
                for date_str in future_dates:
                    day_of_week = DateUtil.get_day_of_week(date_str)
                    
                    # 获取可用时间槽
                    available_slots = self.get_available_time_slots(d_id, c_id, date_str)
                    
                    if available_slots:
                        for slot in available_slots:
                            time_str = DateUtil.get_time_slot_str(slot)
                            print(f"{option_index:2}. {date_str:<12} {day_of_week:<10} {clinic.name:<15} {doctor.full_name:<15} {time_str}")
                            available_options.append((date_str, slot, d_id, c_id))
                            option_index += 1
        
        if not available_options:
            print("没有找到可用的时间槽")
            self.wait_for_key()
            return None
        
        print("\n请选择时间槽编号，或输入0返回，按回车默认选择第一个: ", end="")
        choice = input()
        
        if choice == "":
            return available_options[0]  # 默认选择第一个可用时间槽
        
        if choice == "0":
            return None
        
        try:
            slot_index = int(choice) - 1
            if 0 <= slot_index < len(available_options):
                return available_options[slot_index]
            else:
                print("无效的时间槽编号")
                self.wait_for_key()
                return None
        except ValueError:
            print("请输入有效的数字")
            self.wait_for_key()
            return None
    
    def make_appointment(self, user: User) -> None:
        """预约流程
        
        Args:
            user (User): 当前用户
        """
        # 选择可用时间槽
        slot_info = self.show_available_slots()
        if not slot_info:
            return
        
        date, time_slot, doctor_id, clinic_id = slot_info
        
        doctor = self.__doctor_repo.get_by_id(doctor_id)
        clinic = self.__clinic_repo.get_by_id(clinic_id)
        
        # 输入预约原因
        self.print_header("预约信息")
        print(f"诊所: {clinic.name}")
        print(f"医生: {doctor.full_name}")
        print(f"日期: {date}")
        print(f"时间: {DateUtil.get_time_slot_str(time_slot)}")
        
        reason = input("\n请输入预约原因 (按回车默认为'常规预约'): ")
        if reason == "":
            reason = "常规预约"  # 默认预约原因
        
        # 确认预约
        print("\n请确认预约信息 (Y/N，按回车默认为Y): ", end="")
        confirm = input().strip().upper()
        
        if confirm == "" or confirm == "Y":
            # 创建预约记录
            appointment = Appointment(
                user_id=user.id,
                doctor_id=doctor_id,
                clinic_id=clinic_id,
                date=date,
                time_slot=time_slot,
                reason=reason,
                status="Scheduled"
            )
            
            try:
                # 添加预约
                appointment = self.__appointment_repo.add_appointment(appointment)
                
                # 创建通知
                notification = Notification(
                    user_id=user.id,
                    message=f"您已成功预约 {date} {DateUtil.get_time_slot_str(time_slot)} 在 {clinic.name} 与 {doctor.full_name} 的就诊。",
                    date=DateUtil.get_current_date(),
                    read=False
                )
                
                self.__notification_repo.add(notification)
                
                print("\n预约成功！")
                print(f"预约ID: {appointment.id}")
            except ValueError as e:
                print(f"\n预约失败: {str(e)}")
        else:
            print("预约已取消")
            
        self.wait_for_key()
    
    def show_appointments(self, user: User, future_only: bool = False, history_only: bool = False) -> None:
        """显示预约列表
        
        Args:
            user (User): 当前用户
            future_only (bool): 是否只显示未来预约
            history_only (bool): 是否只显示历史预约
        """
        title = "我的预约"
        if future_only:
            title = "即将到来的预约"
        elif history_only:
            title = "历史预约"
            
        self.print_header(title)
        
        # 获取预约列表
        appointments = self.__appointment_repo.get_by_user(user.id)
        
        if not appointments:
            print("您没有预约记录")
            self.wait_for_key()
            return
        
        # 筛选预约
        today = DateUtil.get_current_date()
        filtered_appointments = []
        
        for appointment in appointments:
            if future_only and appointment.date < today:
                continue
            if history_only and appointment.date >= today:
                continue
            filtered_appointments.append(appointment)
        
        if not filtered_appointments:
            print("没有符合条件的预约记录")
            self.wait_for_key()
            return
        
        print(f"{'ID':<5}{'日期':<15}{'时间':<20}{'诊所':<15}{'医生':<15}{'状态':<15}")
        print("-" * 85)
        
        for appointment in filtered_appointments:
            clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
            doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
            
            clinic_name = clinic.name if clinic else "未知诊所"
            doctor_name = doctor.full_name if doctor else "未知医生"
            time_str = DateUtil.get_time_slot_str(appointment.time_slot)
            
            print(f"{appointment.id:<5}{appointment.date:<15}{time_str:<20}{clinic_name:<15}{doctor_name:<15}{appointment.status:<15}")
        
        print("\n请选择预约ID查看详情，或输入0返回，按回车默认返回: ", end="")
        choice = input()
        
        if choice == "":
            return
        
        if choice == "0":
            return
        
        try:
            appointment_id = int(choice)
            appointment = self.__appointment_repo.get_by_id(appointment_id)
            
            if appointment and appointment.user_id == user.id:
                self.show_appointment_details(appointment)
            else:
                print("无效的预约ID或您无权查看此预约")
                self.wait_for_key()
        except ValueError:
            print("请输入有效的数字")
            self.wait_for_key()
    
    def show_appointment_details(self, appointment: Appointment) -> None:
        """显示预约详情
        
        Args:
            appointment (Appointment): 预约实体
        """
        self.print_header("预约详情")
        
        clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
        doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
        
        print(f"预约ID: {appointment.id}")
        print(f"用户ID: {appointment.user_id}")
        # 尝试获取用户信息以显示更多详情
        try:
            user_repo = UserRepository()
            user = user_repo.get_by_id(appointment.user_id)
            if user:
                print(f"患者姓名: {user.name}")
                print(f"患者邮箱: {user.email}")
        except:
            pass  # 如果无法获取用户信息，则不显示
        print(f"日期: {appointment.date}")
        print(f"时间: {DateUtil.get_time_slot_str(appointment.time_slot)}")
        print(f"诊所: {clinic.name if clinic else '未知'}")
        print(f"诊所地址: {clinic.address if clinic else '未知'}")
        print(f"医生: {doctor.full_name if doctor else '未知'}")
        print(f"预约原因: {appointment.reason}")
        print(f"状态: {appointment.status}")
        
        # 只有未完成的预约才能取消
        if appointment.is_scheduled() and appointment.date >= DateUtil.get_current_date():
            print("\n1. 取消预约")
            print("0. 返回")
            
            choice = input("\n请选择操作，按回车默认返回: ")
            
            if choice == "" or choice == "0":
                return
            
            if choice == "1":
                self.cancel_appointment(appointment)
        else:
            self.wait_for_key()
    
    def cancel_appointment(self, appointment: Appointment) -> None:
        """取消预约
        
        Args:
            appointment (Appointment): 预约实体
        """
        print("\n确认取消预约 (Y/N，按回车默认为N): ", end="")
        confirm = input().strip().upper()
        
        if confirm == "":
            print("操作已取消")
            self.wait_for_key()
            return
        
        if confirm != "Y":
            print("操作已取消")
            self.wait_for_key()
            return
        
        # 取消预约
        if self.__appointment_repo.cancel_appointment(appointment):
            # 创建通知
            notification = Notification(
                user_id=appointment.user_id,
                message=f"您已取消 {appointment.date} {DateUtil.get_time_slot_str(appointment.time_slot)} 的预约。",
                date=DateUtil.get_current_date(),
                read=False
            )
            
            self.__notification_repo.add(notification)
            
            print("\n预约已成功取消")
        else:
            print("\n取消预约失败，可能预约已被取消")
        
        self.wait_for_key()
    
    def search_appointments(self, user: User) -> None:
        """搜索预约
        
        Args:
            user (User): 当前用户
        """
        self.print_header("搜索预约")
        
        print("请选择筛选条件:")
        print("1. 按诊所筛选")
        print("2. 按医生筛选")
        print("3. 按日期筛选")
        print("4. 按诊所和医生筛选")
        print("5. 按诊所和日期筛选")
        print("6. 按医生和日期筛选")
        print("7. 按诊所、医生和日期筛选")
        print("0. 返回")
        
        choice = input("\n请选择: ")
        
        if choice == "0":
            return
        
        params = {}
        
        if choice in ["1", "4", "5", "7"]:
            clinic_id = self.get_clinic_selection()
            if clinic_id == -1:
                return
            params['clinic_id'] = clinic_id
        
        if choice in ["2", "4", "6", "7"]:
            doctor_id = self.get_doctor_selection(params.get('clinic_id'))
            if doctor_id == -1:
                return
            params['doctor_id'] = doctor_id
        
        if choice in ["3", "5", "6", "7"]:
            date = self.get_date_selection(future_only=False)
            if date == -1:
                return
            params['date'] = date
        
        self.show_filtered_appointments(user, params)
    
    def show_filtered_appointments(self, user: User, params: Dict[str, Any]) -> None:
        """显示筛选后的预约列表
        
        Args:
            user (User): 当前用户
            params (Dict[str, Any]): 筛选参数
        """
        self.print_header("筛选结果")
        
        # 获取当前用户的预约
        appointments = self.__appointment_repo.get_by_user(user.id)
        
        # 筛选预约
        filtered_appointments = []
        for appointment in appointments:
            if 'clinic_id' in params and params['clinic_id'] is not None and appointment.clinic_id != params['clinic_id']:
                continue
            if 'doctor_id' in params and params['doctor_id'] is not None and appointment.doctor_id != params['doctor_id']:
                continue
            if 'date' in params and params['date'] is not None and appointment.date != params['date']:
                continue
            filtered_appointments.append(appointment)
        
        if not filtered_appointments:
            print("没有符合条件的预约")
            self.wait_for_key()
            return
        
        print(f"{'ID':<5}{'日期':<15}{'时间':<20}{'诊所':<15}{'医生':<15}{'状态':<15}")
        print("-" * 85)
        
        for appointment in filtered_appointments:
            clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
            doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
            
            clinic_name = clinic.name if clinic else "未知诊所"
            doctor_name = doctor.full_name if doctor else "未知医生"
            time_str = DateUtil.get_time_slot_str(appointment.time_slot)
            
            print(f"{appointment.id:<5}{appointment.date:<15}{time_str:<20}{clinic_name:<15}{doctor_name:<15}{appointment.status:<15}")
        
        print("\n请选择预约ID查看详情，或输入0返回，按回车默认返回: ", end="")
        choice = input()
        
        if choice == "":
            return
        
        if choice == "0":
            return
        
        try:
            appointment_id = int(choice)
            appointment = self.__appointment_repo.get_by_id(appointment_id)
            
            if appointment and appointment.user_id == user.id:
                self.show_appointment_details(appointment)
            else:
                print("无效的预约ID或您无权查看此预约")
                self.wait_for_key()
        except ValueError:
            print("请输入有效的数字")
            self.wait_for_key()
    
    def run_appointment_menu(self, user: User) -> None:
        """运行预约菜单
        
        Args:
            user (User): 当前用户
        """
        while True:
            self.print_header(f"预约菜单 - {user.name}")
            
            print("1. 查询可用时间槽并预约")
            print("2. 查看我的所有预约")
            print("3. 查看即将到来的预约")
            print("4. 查看历史预约")
            print("5. 搜索预约")
            print("0. 返回")
            
            choice = input("\n请选择操作: ")
            
            if choice == "1":
                self.make_appointment(user)
            elif choice == "2":
                self.show_appointments(user)
            elif choice == "3":
                self.show_appointments(user, future_only=True)
            elif choice == "4":
                self.show_appointments(user, history_only=True)
            elif choice == "5":
                self.search_appointments(user)
            elif choice == "0":
                break
            else:
                print("无效的选择")
                self.wait_for_key()
    
    def run(self):
        """运行预约菜单（兼容UserController的调用方式）"""
        if self.__current_user is None:
            print("错误：未提供用户信息")
            return
            
        self.run_appointment_menu(self.__current_user)
