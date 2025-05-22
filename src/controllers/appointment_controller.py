#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
预约控制器类 - 处理预约相关的用户界面和交互
"""

import os
from typing import Optional, Dict, Any, Tuple, List

from src.entities.user import User
from src.services.appointment_service import AppointmentService
from src.utils.date_util import DateUtil

class AppointmentController:
    """预约控制器类 - 处理预约相关的用户界面和交互"""
    
    def __init__(self, user=None):
        """初始化预约控制器
        
        Args:
            user (User, optional): 当前用户. Defaults to None.
        """
        self.__appointment_service = AppointmentService()
        self.__current_user = user
        self.__should_return_to_main = False  # 是否返回主菜单标志
        self.__DateUtil = DateUtil()
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
    
    def print_navigation_options(self, has_default=True, default_text=""):
        """打印导航选项
        
        Args:
            has_default (bool): 是否有默认选项
            default_text (str): 默认选项文本
        """
        print("\n0. 返回上一级")
        print("-. 返回主菜单")
        if has_default and default_text:
            print(f"直接按回车{default_text}")
    
    def handle_navigation_choice(self, choice: str) -> int:
        """处理导航选择
        
        Args:
            choice (str): 用户输入
            
        Returns:
            int: 0表示返回上一级，-1表示返回主菜单，其他值为实际选择
        """
        if choice == "-":
            self.__should_return_to_main = True
            return -1
        return 0 if choice == "0" else 1
    
    def get_clinic_selection(self, default_option: bool = True) -> Optional[int]:
        """显示诊所选择界面
        
        Args:
            default_option (bool): 是否显示默认选项（所有诊所）
            
        Returns:
            Optional[int]: 选择的诊所ID，如果选择所有诊所则返回None
                          返回-1表示返回上一级，如果self.__should_return_to_main为True则表示返回主菜单
        """
        self.print_header("选择诊所")
        
        clinics = self.__appointment_service.get_all_clinics()
        
        if not clinics:
            print("没有找到诊所记录")
            self.wait_for_key()
            return -1
        
        print(f"{'ID':<5}{'名称':<15}{'区域':<10}{'地址':<20}{'电话':<15}")
        print("-" * 65)
        
        for clinic in clinics:
            print(f"{clinic.id:<5}{clinic.name:<15}{clinic.suburb:<10}{clinic.address:<20}{clinic.phone:<15}")
        
        option_text = "\n请选择诊所ID"
        if default_option:
            option_text += "，或输入0查看所有诊所/返回上一级"
        else:
            option_text += "，或输入0返回上一级"
        option_text += "，输入-返回主菜单"
        option_text += "，直接按回车默认查看所有诊所: "
        
        print(option_text, end="")
        choice = input()
        
        if choice == "":
            return None  # 直接按回车默认查看所有诊所
        
        if choice == "-":
            self.__should_return_to_main = True
            return -1
        
        if choice == "0":
            return -1 if not default_option else None
        
        try:
            clinic_id = int(choice)
            selected_clinic = self.__appointment_service.get_clinic_by_id(clinic_id)
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
                          返回-1表示返回上一级，如果self.__should_return_to_main为True则表示返回主菜单
        """
        self.print_header("选择医生")
        
        if clinic_id:
            doctors = self.__appointment_service.get_doctors_by_clinic(clinic_id)
            print(f"诊所 {clinic_id} 的医生列表:")
        else:
            doctors = self.__appointment_service.get_all_doctors()
            print("所有医生列表:")
        
        if not doctors:
            print("没有找到医生记录")
            self.wait_for_key()
            return -1
        
        print(f"{'ID':<5}{'姓名':<15}{'电子邮箱':<25}{'专业':<20}")
        print("-" * 65)
        
        for doctor in doctors:
            specialisation = ", ".join(doctor.specialisation)
            print(f"{doctor.id:<5}{doctor.full_name:<15}{doctor.email:<25}{specialisation:<20}")
        
        option_text = "\n请选择医生ID"
        if default_option:
            option_text += "，或输入0查看所有医生/返回上一级"
        else:
            option_text += "，或输入0返回上一级"
        option_text += "，输入-返回主菜单"
        option_text += "，直接按回车默认查看所有医生: "
        
        print(option_text, end="")
        choice = input()
        
        if choice == "":
            return None  # 直接按回车默认查看所有医生
        
        if choice == "-":
            self.__should_return_to_main = True
            return -1
        
        if choice == "0":
            return -1 if not default_option else None
        
        try:
            doctor_id = int(choice)
            selected_doctor = self.__appointment_service.get_doctor_by_id(doctor_id)
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
                          返回-1表示返回上一级，如果self.__should_return_to_main为True则表示返回主菜单
        """
        self.print_header("选择日期")
        
        today = self.__appointment_service.get_current_date()

        if future_only:
            dates = self.__appointment_service.get_date_range(today, 7)
            print("未来7天的日期:")
        else:
            start_past = self.__DateUtil.shift_date(today, -7)
            past_dates = self.__appointment_service.get_date_range(start_past, 7)
            future_dates = self.__appointment_service.get_date_range(today, 7)
            dates = past_dates + future_dates
            print("可选日期(过去7天和未来7天):")
        
        print(f"{'日期':<15}{'星期':<10}")
        print("-" * 25)
        
        for date in dates:
            day_of_week = self.__appointment_service.get_day_of_week(date)
            print(f"{date:<15}{day_of_week:<10}")
        
        option_text = "\n请输入日期(YYYY-MM-DD)"
        if default_option:
            option_text += "，或输入0查看所有日期/返回上一级"
        else:
            option_text += "，或输入0返回上一级"
        option_text += "，输入-返回主菜单"
        option_text += f"，直接按回车默认选择今天({today}): "
        
        print(option_text, end="")
        choice = input()
        
        if choice == "":
            return today  # 直接按回车默认选择今天
        
        if choice == "-":
            self.__should_return_to_main = True
            return -1
        
        if choice == "0":
            return -1 if not default_option else None
        
        if not self.__appointment_service.is_valid_date(choice):
            print("无效的日期格式，请使用YYYY-MM-DD格式")
            self.wait_for_key()
            return self.get_date_selection(future_only, default_option)
        
        if future_only and choice < today:
            print("请选择未来的日期")
            self.wait_for_key()
            return self.get_date_selection(future_only, default_option)
        
        return choice
    
    def show_available_slots(self, params: Dict[str, Any] = None) -> Optional[Tuple[str, int, int, int]]:
        """显示可用的时间槽
        
        Args:
            params (Dict[str, Any], optional): 参数字典，可包含doctor_id, clinic_id, date
            
        Returns:
            Optional[Tuple[str, int, int, int]]: (日期, 时间槽, 医生ID, 诊所ID)元组
                                               如果用户取消则返回None
                                               如果self.__should_return_to_main为True则表示返回主菜单
        """
        params = params or {}
        
        # 获取参数
        clinic_id = params.get('clinic_id')
        doctor_id = params.get('doctor_id')
        date = params.get('date')
        
        # 如果未指定诊所，让用户选择
        if clinic_id is None:
            clinic_id = self.get_clinic_selection()
            if clinic_id == -1:  # 用户取消或返回主菜单
                return None
        
        # 如果未指定医生，让用户选择
        if doctor_id is None:
            doctor_id = self.get_doctor_selection(clinic_id)
            if doctor_id == -1:  # 用户取消或返回主菜单
                return None
        
        # 如果未指定日期，让用户选择
        if date is None:
            date = self.get_date_selection()
            if date == -1:  # 用户取消或返回主菜单
                return None
        
        # 如果未指定任何筛选条件，需要用户至少选择一个
        if clinic_id is None and doctor_id is None and date is None:
            print("请至少选择一个筛选条件(诊所、医生或日期)")
            self.wait_for_key()
            return self.show_available_slots()
        
        self.print_header("可用时间槽")
        
        # 获取可用时间槽
        available_slots_data = self.__appointment_service.get_available_slots_data(clinic_id, doctor_id, date)
        
        if not available_slots_data:
            print("没有找到可用的时间槽")
            self.wait_for_key()
            return None
        
        print("可用时间槽:")
        print(f"{'日期':<15}{'星期':<10}{'诊所':<15}{'医生':<15}{'可用时间'}")
        print("-" * 85)
        
        option_index = 1
        for date_str, slot, d_id, c_id, clinic_name, doctor_name, day_of_week, time_str in available_slots_data:
            print(f"{option_index:2}. {date_str:<12} {day_of_week:<10} {clinic_name:<15} {doctor_name:<15} {time_str}")
            option_index += 1
        
        print("\n请选择时间槽编号，或输入0返回上一级，输入-返回主菜单，按回车默认选择第一个: ", end="")
        choice = input()
        
        if choice == "":
            return available_slots_data[0][:4]  # 默认选择第一个可用时间槽 (仅返回日期, 时间槽, 医生ID, 诊所ID)
        
        if choice == "-":
            self.__should_return_to_main = True
            return None
        
        if choice == "0":
            return None
        
        try:
            slot_index = int(choice) - 1
            if 0 <= slot_index < len(available_slots_data):
                return available_slots_data[slot_index][:4]  # 返回选中的时间槽
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
        
        doctor = self.__appointment_service.get_doctor_by_id(doctor_id)
        clinic = self.__appointment_service.get_clinic_by_id(clinic_id)
        
        # 输入预约原因
        self.print_header("预约信息")
        print(f"诊所: {clinic.name}")
        print(f"医生: {doctor.full_name}")
        print(f"日期: {date}")
        print(f"时间: {self.__appointment_service.get_time_slot_str(time_slot)}")
        
        reason = input("\n请输入预约原因 (按回车默认为'常规预约'): ")
        if reason == "":
            reason = "常规预约"  # 默认预约原因
        
        # 确认预约
        print("\n请确认预约信息 (Y/N)，或输入0返回上一级，输入-返回主菜单，按回车默认为Y: ", end="")
        confirm = input().strip().upper()
        
        if confirm == "-":
            self.__should_return_to_main = True
            return
            
        if confirm == "0":
            return
            
        if confirm == "" or confirm == "Y":
            try:
                # 创建预约
                appointment = self.__appointment_service.make_appointment(
                    user.id, doctor_id, clinic_id, date, time_slot, reason
                )
                
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
        appointments = self.__appointment_service.get_user_appointments(user.id, future_only, history_only)
        
        if not appointments:
            print("您没有预约记录" if not future_only and not history_only else "没有符合条件的预约记录")
            self.wait_for_key()
            return
        
        print(f"{'ID':<5}{'日期':<15}{'时间':<20}{'诊所':<15}{'医生':<15}{'状态':<15}")
        print("-" * 85)
        
        for appointment in appointments:
            print(f"{appointment['id']:<5}{appointment['date']:<15}{appointment['time_str']:<20}{appointment['clinic_name']:<15}{appointment['doctor_name']:<15}{appointment['status']:<15}")
        
        print("\n请选择预约ID查看详情，或输入0返回上一级，输入-返回主菜单，按回车默认返回: ", end="")
        choice = input()
        
        if choice == "-":
            self.__should_return_to_main = True
            return
            
        if choice == "" or choice == "0":
            return
        
        try:
            appointment_id = int(choice)
            appointment_details = self.__appointment_service.get_appointment_details(appointment_id)
            
            if appointment_details and appointment_details['user_id'] == user.id:
                self.show_appointment_details(appointment_details)
            else:
                print("无效的预约ID或您无权查看此预约")
                self.wait_for_key()
        except ValueError:
            print("请输入有效的数字")
            self.wait_for_key()
    
    def show_appointment_details(self, appointment_details: Dict) -> None:
        """显示预约详情
        
        Args:
            appointment_details (Dict): 预约详情字典
        """
        self.print_header("预约详情")
        
        print(f"预约ID: {appointment_details['id']}")
        print(f"用户ID: {appointment_details['user_id']}")
        print(f"患者姓名: {appointment_details['user_name']}")
        print(f"患者邮箱: {appointment_details['user_email']}")
        print(f"日期: {appointment_details['date']}")
        print(f"时间: {appointment_details['time_str']}")
        print(f"诊所: {appointment_details['clinic_name']}")
        print(f"诊所地址: {appointment_details['clinic_address']}")
        print(f"医生: {appointment_details['doctor_name']}")
        print(f"预约原因: {appointment_details['reason']}")
        print(f"状态: {appointment_details['status']}")
        
        # 只有未完成的预约才能取消
        if appointment_details['can_cancel']:
            print("\n1. 取消预约")
            print("0. 返回上一级")
            print("-. 返回主菜单")
            
            choice = input("\n请选择操作，按回车默认返回: ")
            
            if choice == "-":
                self.__should_return_to_main = True
                return
                
            if choice == "" or choice == "0":
                return
            
            if choice == "1":
                self.cancel_appointment(appointment_details['appointment_obj'])
        else:
            print("\n0. 返回上一级")
            print("-. 返回主菜单")
            choice = input("\n请选择操作，按回车默认返回: ")
            
            if choice == "-":
                self.__should_return_to_main = True
                return
                
            self.wait_for_key()
    
    def cancel_appointment(self, appointment) -> None:
        """取消预约
        
        Args:
            appointment: 预约对象
        """
        print("\n确认取消预约 (Y/N)，或输入0返回上一级，输入-返回主菜单，按回车默认为N: ", end="")
        confirm = input().strip().upper()
        
        if confirm == "-":
            self.__should_return_to_main = True
            return
            
        if confirm == "0" or confirm == "":
            print("操作已取消")
            self.wait_for_key()
            return
        
        if confirm != "Y":
            print("操作已取消")
            self.wait_for_key()
            return
        
        # 取消预约
        if self.__appointment_service.cancel_appointment(appointment):
            print("\n预约已成功取消")
        else:
            print("\n取消预约失败，可能预约已被取消")
        
        self.wait_for_key()

    def _show_all_appointments(self) -> None:
        """显示系统所有预约（管理员专用）"""
        self.print_header("所有预约")
        appointments = self.__appointment_service.get_all_appointments()

        if not appointments:
            print("暂无预约记录")
            self.wait_for_key()
            return

        print(f"{'ID':<5}{'用户ID':<8}{'日期':<12}{'时间':<18}{'医生':<15}{'诊所':<15}{'状态':<12}")
        print("-" * 90)
        for appt in appointments:
            print(f"{appt['id']:<5}{appt['user_id']:<8}{appt['date']:<12}{appt['time_str']:<18}"
                  f"{appt['doctor_name']:<15}{appt['clinic_name']:<15}{appt['status']:<12}")
        self.wait_for_key()

    def _cancel_by_id(self) -> None:
        """管理员手动取消任意预约"""
        try:
            appt_id = int(input("\n输入要取消的预约ID（0返回）: ").strip())
            if appt_id == 0:
                return
            appointment = self.__appointment_service.get_appointment_by_id(appt_id)
            if not appointment or not appointment.is_scheduled():
                print("预约不存在或状态不可取消")
                self.wait_for_key()
                return
            if input("确认取消该预约？(Y/N): ").strip().upper() == "Y":
                if self.__appointment_service.cancel_appointment(appointment):
                    print("已取消")
                else:
                    print("取消失败")
            else:
                print("操作取消")
        except ValueError:
            print("请输入有效的数字")
        self.wait_for_key()

    def _search_as_admin(self) -> None:
        """管理员筛选预约（不限制 user_id）"""
        dummy_user = User(id=-1)  # 用于绕过 user_id 限制
        self.search_appointments(dummy_user)

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
        print("0. 返回上一级")
        print("-. 返回主菜单")
        
        choice = input("\n请选择: ")
        
        if choice == "-":
            self.__should_return_to_main = True
            return
            
        if choice == "0":
            return
        
        params = {}
        
        if choice in ["1", "4", "5", "7"]:
            clinic_id = self.get_clinic_selection()
            if clinic_id == -1:
                if self.__should_return_to_main:
                    return
                return
            params['clinic_id'] = clinic_id
        
        if choice in ["2", "4", "6", "7"]:
            doctor_id = self.get_doctor_selection(params.get('clinic_id'))
            if doctor_id == -1:
                if self.__should_return_to_main:
                    return
                return
            params['doctor_id'] = doctor_id
        
        if choice in ["3", "5", "6", "7"]:
            date = self.get_date_selection(future_only=False)
            if date == -1:
                if self.__should_return_to_main:
                    return
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
        
        # 获取筛选后的预约
        appointments = self.__appointment_service.filter_appointments(user.id, params)
        
        if not appointments:
            print("没有符合条件的预约")
            self.wait_for_key()
            return
        
        print(f"{'ID':<5}{'日期':<15}{'时间':<20}{'诊所':<15}{'医生':<15}{'状态':<15}")
        print("-" * 85)
        
        for appointment in appointments:
            print(f"{appointment['id']:<5}{appointment['date']:<15}{appointment['time_str']:<20}{appointment['clinic_name']:<15}{appointment['doctor_name']:<15}{appointment['status']:<15}")
        
        print("\n请选择预约ID查看详情，或输入0返回上一级，输入-返回主菜单，按回车默认返回: ", end="")
        choice = input()
        
        if choice == "-":
            self.__should_return_to_main = True
            return
            
        if choice == "" or choice == "0":
            return
        
        try:
            appointment_id = int(choice)
            appointment_details = self.__appointment_service.get_appointment_details(appointment_id)
            
            if appointment_details and appointment_details['user_id'] == user.id:
                self.show_appointment_details(appointment_details)
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
        self.__should_return_to_main = False  # 重置返回主菜单标志
        
        while True:
            if self.__should_return_to_main:
                break
                
            self.print_header(f"预约菜单 - {user.name}")
            
            print("1. 查询可用时间槽并预约")
            print("2. 查看我的所有预约")
            print("3. 查看即将到来的预约")
            print("4. 查看历史预约")
            print("5. 搜索预约")
            print("0. 返回上一级")
            print("-. 返回主菜单")
            
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
            elif choice == "-":
                self.__should_return_to_main = True
                break
            else:
                print("无效的选择")
                self.wait_for_key()

    def run_admin_menu(self) -> None:
        """管理员预约管理菜单"""
        while True:
            self.print_header("预约管理 - 管理员")
            print("1. 查看全部预约")
            print("2. 按条件筛选预约")
            print("3. 按ID取消预约")
            print("0. 返回上一级")
            choice = input("\n请选择操作: ").strip()

            if choice == "1":
                self._show_all_appointments()
            elif choice == "2":
                self._search_as_admin()
            elif choice == "3":
                self._cancel_by_id()
            elif choice == "0":
                break
            else:
                print("无效选项")
                self.wait_for_key()

    def run(self):
        """运行预约菜单（兼容UserController的调用方式）"""
        if self.__current_user is None:
            print("错误：未提供用户信息")
            return
            
        self.run_appointment_menu(self.__current_user)
        
        # 返回标志，供调用者判断是返回上一级还是返回主菜单
        return self.__should_return_to_main
