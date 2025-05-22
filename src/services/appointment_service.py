#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
预约服务类 - 处理预约相关的业务逻辑
"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime

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


class AppointmentService:
    """预约服务类 - 处理预约相关的业务逻辑"""
    
    def __init__(self):
        """初始化预约服务"""
        self.__appointment_repo = AppointmentRepository()
        self.__clinic_repo = ClinicRepository()
        self.__doctor_repo = DoctorRepository()
        self.__schedule_repo = DoctorScheduleRepository()
        self.__notification_repo = NotificationRepository()
        self.__user_repo = UserRepository()
    
    def get_all_clinics(self) -> List:
        """获取所有诊所
        
        Returns:
            List: 诊所列表
        """
        return self.__clinic_repo.get_all()
    
    def get_clinic_by_id(self, clinic_id: int):
        """根据ID获取诊所
        
        Args:
            clinic_id (int): 诊所ID
            
        Returns:
            Clinic: 诊所对象
        """
        return self.__clinic_repo.get_by_id(clinic_id)
    
    def get_all_doctors(self) -> List:
        """获取所有医生
        
        Returns:
            List: 医生列表
        """
        return self.__doctor_repo.get_all()
    
    def get_doctors_by_clinic(self, clinic_id: int) -> List:
        """获取指定诊所的医生
        
        Args:
            clinic_id (int): 诊所ID
            
        Returns:
            List: 医生列表
        """
        return self.__doctor_repo.get_by_clinic(clinic_id)
    
    def get_doctor_by_id(self, doctor_id: int):
        """根据ID获取医生
        
        Args:
            doctor_id (int): 医生ID
            
        Returns:
            Doctor: 医生对象
        """
        return self.__doctor_repo.get_by_id(doctor_id)
    
    def get_date_range(self, start_date: str, days: int) -> List[str]:
        """获取日期范围
        
        Args:
            start_date (str): 开始日期
            days (int): 天数
            
        Returns:
            List[str]: 日期列表
        """
        return DateUtil.get_date_range(start_date, days)
    
    def get_current_date(self) -> str:
        """获取当前日期
        
        Returns:
            str: 当前日期
        """
        return DateUtil.get_current_date()
    
    def get_day_of_week(self, date: str) -> str:
        """获取星期几
        
        Args:
            date (str): 日期
            
        Returns:
            str: 星期几
        """
        return DateUtil.get_day_of_week(date)
    
    def is_valid_date(self, date_str: str) -> bool:
        """检查日期格式是否有效
        
        Args:
            date_str (str): 日期字符串
            
        Returns:
            bool: 日期格式是否有效
        """
        return DateUtil.is_valid_date(date_str)
    
    def get_time_slot_str(self, slot: int) -> str:
        """获取时间槽的字符串表示
        
        Args:
            slot (int): 时间槽索引
            
        Returns:
            str: 时间槽字符串
        """
        return DateUtil.get_time_slot_str(slot)
    
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
    
    def get_available_slots_data(self, clinic_id: Optional[int] = None, 
                               doctor_id: Optional[int] = None, 
                               date: Optional[str] = None) -> List[Tuple]:
        """获取可用时间槽数据
        
        Args:
            clinic_id (Optional[int]): 诊所ID
            doctor_id (Optional[int]): 医生ID
            date (Optional[str]): 日期
            
        Returns:
            List[Tuple]: (日期, 时间槽, 医生ID, 诊所ID, 诊所名称, 医生姓名, 星期几, 时间字符串)元组列表
        """
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
        
        available_slots_data = []
        
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
                            available_slots_data.append(
                                (date_str, slot, d_id, c_id, clinic.name, doctor.full_name, day_of_week, time_str)
                            )
        
        return available_slots_data
    
    def make_appointment(self, user_id: int, doctor_id: int, clinic_id: int, 
                       date: str, time_slot: int, reason: str) -> Appointment:
        """创建预约
        
        Args:
            user_id (int): 用户ID
            doctor_id (int): 医生ID
            clinic_id (int): 诊所ID
            date (str): 日期
            time_slot (int): 时间槽
            reason (str): 预约原因
            
        Returns:
            Appointment: 创建的预约
            
        Raises:
            ValueError: 如果时间槽不可用
        """
        # 创建预约记录
        appointment = Appointment(
            user_id=user_id,
            doctor_id=doctor_id,
            clinic_id=clinic_id,
            date=date,
            time_slot=time_slot,
            reason=reason,
            status="Scheduled"
        )
        
        # 添加预约
        appointment = self.__appointment_repo.add_appointment(appointment)
        
        # 获取相关实体用于通知
        doctor = self.__doctor_repo.get_by_id(doctor_id)
        clinic = self.__clinic_repo.get_by_id(clinic_id)
        
        # 创建通知
        notification = Notification(
            user_id=user_id,
            message=f"您已成功预约 {date} {DateUtil.get_time_slot_str(time_slot)} 在 {clinic.name} 与 {doctor.full_name} 的就诊。",
            date=DateUtil.get_current_date(),
            read=False
        )
        
        self.__notification_repo.add(notification)
        
        return appointment
    
    def get_user_appointments(self, user_id: int, future_only: bool = False, history_only: bool = False) -> List[Dict]:
        """获取用户预约列表
        
        Args:
            user_id (int): 用户ID
            future_only (bool): 是否只返回未来预约
            history_only (bool): 是否只返回历史预约
            
        Returns:
            List[Dict]: 预约信息字典列表
        """
        # 获取预约列表
        appointments = self.__appointment_repo.get_by_user(user_id)
        
        if not appointments:
            return []
        
        # 筛选预约
        today = DateUtil.get_current_date()
        filtered_appointments = []
        
        for appointment in appointments:
            if future_only and appointment.date < today:
                continue
            if history_only and appointment.date >= today:
                continue
            
            clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
            doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
            
            clinic_name = clinic.name if clinic else "未知诊所"
            doctor_name = doctor.full_name if doctor else "未知医生"
            time_str = DateUtil.get_time_slot_str(appointment.time_slot)
            
            filtered_appointments.append({
                "id": appointment.id,
                "date": appointment.date,
                "time_slot": appointment.time_slot,
                "time_str": time_str,
                "clinic_id": appointment.clinic_id,
                "clinic_name": clinic_name,
                "doctor_id": appointment.doctor_id,
                "doctor_name": doctor_name,
                "reason": appointment.reason,
                "status": appointment.status,
                "appointment_obj": appointment  # 包含原始对象，便于操作
            })
        
        return filtered_appointments
    
    def get_appointment_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """根据ID获取预约
        
        Args:
            appointment_id (int): 预约ID
            
        Returns:
            Optional[Appointment]: 预约对象，如果不存在则返回None
        """
        return self.__appointment_repo.get_by_id(appointment_id)
    
    def get_appointment_details(self, appointment_id: int) -> Optional[Dict]:
        """获取预约详情
        
        Args:
            appointment_id (int): 预约ID
            
        Returns:
            Optional[Dict]: 预约详情字典，如果不存在则返回None
        """
        appointment = self.__appointment_repo.get_by_id(appointment_id)
        
        if not appointment:
            return None
        
        clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
        doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
        user = self.__user_repo.get_by_id(appointment.user_id)
        
        details = {
            "id": appointment.id,
            "user_id": appointment.user_id,
            "user_name": user.name if user else "未知用户",
            "user_email": user.email if user else "未知邮箱",
            "date": appointment.date,
            "time_slot": appointment.time_slot,
            "time_str": DateUtil.get_time_slot_str(appointment.time_slot),
            "clinic_id": appointment.clinic_id,
            "clinic_name": clinic.name if clinic else "未知诊所",
            "clinic_address": clinic.address if clinic else "未知地址",
            "doctor_id": appointment.doctor_id,
            "doctor_name": doctor.full_name if doctor else "未知医生",
            "reason": appointment.reason,
            "status": appointment.status,
            "can_cancel": appointment.is_scheduled() and appointment.date >= DateUtil.get_current_date(),
            "appointment_obj": appointment  # 包含原始对象，便于操作
        }
        
        return details
    
    def cancel_appointment(self, appointment: Appointment) -> bool:
        """取消预约
        
        Args:
            appointment (Appointment): 预约对象
            
        Returns:
            bool: 是否成功取消
        """
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
            
            return True
        
        return False
    
    def filter_appointments(self, user_id: int, params: Dict[str, Any]) -> List[Dict]:
        """筛选预约
        
        Args:
            user_id (int): 用户ID
            params (Dict[str, Any]): 筛选参数
            
        Returns:
            List[Dict]: 预约信息字典列表
        """
        # 管理员用户（ID为-1）可以查看所有预约
        if user_id == -1:
            appointments = self.__appointment_repo.get_all()
        else:
            # 普通用户只能查看自己的预约
            appointments = self.__appointment_repo.get_by_user(user_id)
        
        # 筛选预约
        filtered_appointments = []
        for appointment in appointments:
            if 'clinic_id' in params and params['clinic_id'] is not None and appointment.clinic_id != params['clinic_id']:
                continue
            if 'doctor_id' in params and params['doctor_id'] is not None and appointment.doctor_id != params['doctor_id']:
                continue
            if 'date' in params and params['date'] is not None and appointment.date != params['date']:
                continue
            
            clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
            doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
            
            clinic_name = clinic.name if clinic else "未知诊所"
            doctor_name = doctor.full_name if doctor else "未知医生"
            time_str = DateUtil.get_time_slot_str(appointment.time_slot)
            
            filtered_appointments.append({
                "id": appointment.id,
                "user_id": appointment.user_id,
                "date": appointment.date,
                "time_slot": appointment.time_slot,
                "time_str": time_str,
                "clinic_id": appointment.clinic_id,
                "clinic_name": clinic_name,
                "doctor_id": appointment.doctor_id,
                "doctor_name": doctor_name,
                "reason": appointment.reason,
                "status": appointment.status,
                "appointment_obj": appointment  # 包含原始对象，便于操作
            })
        
        return filtered_appointments

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

    def get_all_appointments(self) -> List[Dict]:
        """获取系统中所有预约（管理员视图）"""
        appointments = self.__appointment_repo.get_all()

        result = []
        for appointment in appointments:
            clinic = self.__clinic_repo.get_by_id(appointment.clinic_id)
            doctor = self.__doctor_repo.get_by_id(appointment.doctor_id)
            result.append({
                "id": appointment.id,
                "user_id": appointment.user_id,
                "date": appointment.date,
                "time_slot": appointment.time_slot,
                "time_str": DateUtil.get_time_slot_str(appointment.time_slot),
                "clinic_name": clinic.name if clinic else "未知",
                "doctor_name": doctor.full_name if doctor else "未知",
                "status": appointment.status
            })
        return result
