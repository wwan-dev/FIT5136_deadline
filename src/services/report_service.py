#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
报告服务类 - 处理统计报告相关业务逻辑
"""

import os
import csv
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter

from src.entities.appointment import Appointment
from src.entities.doctor import Doctor
from src.entities.clinic import Clinic
from src.repositories.appointment_repository import AppointmentRepository
from src.repositories.doctor_repository import DoctorRepository
from src.repositories.clinic_repository import ClinicRepository

class ReportService:
    """报告服务类"""
    
    def __init__(self):
        """初始化报告服务"""
        self.__appointment_repo = AppointmentRepository()
        self.__doctor_repo = DoctorRepository()
        self.__clinic_repo = ClinicRepository()
    
    def _get_date_range(self, range_type: str, start_date: str = None, end_date: str = None) -> Tuple[str, str]:
        """获取日期范围
        
        Args:
            range_type (str): 范围类型，可选值：'day', 'week', 'month', 'custom'
            start_date (str, optional): 自定义范围起始日期，格式为 "YYYY-MM-DD"
            end_date (str, optional): 自定义范围结束日期，格式为 "YYYY-MM-DD"
            
        Returns:
            Tuple[str, str]: 包含起始日期和结束日期的元组
        """
        today = datetime.now()
        
        if range_type == 'day':
            # 今天
            return today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
        elif range_type == 'week':
            # 本周（过去7天）
            start = today - timedelta(days=7)
            return start.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
        elif range_type == 'month':
            # 本月（过去30天）
            start = today - timedelta(days=30)
            return start.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
        elif range_type == 'custom' and start_date and end_date:
            # 自定义范围
            return start_date, end_date
        else:
            # 默认为今天
            return today.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
    
    def _filter_appointments_by_date_range(self, appointments: List[Appointment], start_date: str, end_date: str) -> List[Appointment]:
        """按日期范围筛选预约
        
        Args:
            appointments (List[Appointment]): 预约列表
            start_date (str): 起始日期，格式为 "YYYY-MM-DD"
            end_date (str): 结束日期，格式为 "YYYY-MM-DD"
            
        Returns:
            List[Appointment]: 筛选后的预约列表
        """
        return [app for app in appointments if start_date <= app.date <= end_date]
    
    def _get_time_slot_display(self, time_slot: int) -> str:
        """获取时间槽显示文本
        
        Args:
            time_slot (int): 时间槽索引
            
        Returns:
            str: 时间槽显示文本
        """
        # 时间槽对应关系（示例）
        time_slots = {
            1: "8:00 AM - 8:30 AM",
            2: "8:30 AM - 9:00 AM",
            3: "9:00 AM - 9:30 AM",
            4: "9:30 AM - 10:00 AM",
            5: "10:00 AM - 10:30 AM",
            6: "10:30 AM - 11:00 AM",
            7: "11:00 AM - 11:30 AM",
            8: "11:30 AM - 12:00 PM",
            9: "12:00 PM - 12:30 PM",
            10: "12:30 PM - 1:00 PM",
            11: "1:00 PM - 1:30 PM",
            12: "1:30 PM - 2:00 PM",
            13: "2:00 PM - 2:30 PM",
            14: "2:30 PM - 3:00 PM",
            15: "3:00 PM - 3:30 PM",
            16: "3:30 PM - 4:00 PM",
        }
        return time_slots.get(time_slot, f"时间槽 {time_slot}")
    
    def generate_doctor_report(self, date_range_type: str, start_date: str = None, end_date: str = None) -> List[Dict[str, Any]]:
        """生成医生接待人数报告
        
        Args:
            date_range_type (str): 日期范围类型，可选值：'day', 'week', 'month', 'custom'
            start_date (str, optional): 自定义范围起始日期，格式为 "YYYY-MM-DD"
            end_date (str, optional): 自定义范围结束日期，格式为 "YYYY-MM-DD"
            
        Returns:
            List[Dict[str, Any]]: 报告数据列表，每个医生一条记录
        """
        # 获取日期范围
        start_date, end_date = self._get_date_range(date_range_type, start_date, end_date)
        
        # 获取所有预约
        all_appointments = self.__appointment_repo.get_all()
        
        # 按日期范围筛选预约
        filtered_appointments = self._filter_appointments_by_date_range(all_appointments, start_date, end_date)
        
        # 按医生ID分组统计
        doctor_stats = defaultdict(lambda: {"count": 0, "reasons": Counter()})
        
        for appointment in filtered_appointments:
            if appointment.is_completed() or appointment.is_scheduled():
                doctor_id = appointment.doctor_id
                doctor_stats[doctor_id]["count"] += 1
                doctor_stats[doctor_id]["reasons"][appointment.reason] += 1
        
        # 获取医生详细信息并整合报告数据
        report_data = []
        
        for doctor_id, stats in doctor_stats.items():
            doctor = self.__doctor_repo.get_by_id(doctor_id)
            if doctor:
                # 获取医生所在诊所的郊区
                clinic_suburbs = []
                for clinic_id in doctor.assigned_clinics:
                    clinic = self.__clinic_repo.get_by_id(clinic_id)
                    if clinic:
                        clinic_suburbs.append(clinic.suburb)
                
                # 处理就诊原因数据
                reasons_list = []
                for reason, count in stats["reasons"].items():
                    reasons_list.append(f"{reason}: {count}")
                
                report_item = {
                    "doctor_id": doctor_id,
                    "doctor_name": doctor.full_name,
                    "clinic_suburbs": ", ".join(clinic_suburbs),
                    "appointment_count": stats["count"],
                    "appointment_reasons": ", ".join(reasons_list)
                }
                report_data.append(report_item)
        
        # 按预约数量降序排序
        report_data.sort(key=lambda x: x["appointment_count"], reverse=True)
        
        return report_data
    
    def generate_clinic_report(self, clinic_id: int, date_range_type: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """生成诊所预约数据报告
        
        Args:
            clinic_id (int): 诊所ID
            date_range_type (str): 日期范围类型，可选值：'day', 'week', 'month', 'custom'
            start_date (str, optional): 自定义范围起始日期，格式为 "YYYY-MM-DD"
            end_date (str, optional): 自定义范围结束日期，格式为 "YYYY-MM-DD"
            
        Returns:
            Dict[str, Any]: 诊所报告数据
        """
        # 获取日期范围
        start_date, end_date = self._get_date_range(date_range_type, start_date, end_date)
        
        # 获取诊所信息
        clinic = self.__clinic_repo.get_by_id(clinic_id)
        if not clinic:
            return {"error": f"找不到ID为 {clinic_id} 的诊所"}
        
        # 获取诊所的所有预约
        clinic_appointments = self.__appointment_repo.get_by_clinic(clinic_id)
        
        # 按日期范围筛选预约
        filtered_appointments = self._filter_appointments_by_date_range(clinic_appointments, start_date, end_date)
        
        # 有效预约（已完成或已安排）
        valid_appointments = [app for app in filtered_appointments 
                             if app.is_completed() or app.is_scheduled()]
        
        # 统计总预约数
        total_appointments = len(valid_appointments)
        
        # 按医生统计预约数
        doctor_stats = defaultdict(int)
        for appointment in valid_appointments:
            doctor_stats[appointment.doctor_id] += 1
        
        # 获取医生详细信息
        doctor_details = []
        for doctor_id, count in doctor_stats.items():
            doctor = self.__doctor_repo.get_by_id(doctor_id)
            if doctor:
                doctor_details.append({
                    "doctor_id": doctor_id,
                    "doctor_name": doctor.full_name,
                    "appointment_count": count
                })
        
        # 按预约数量降序排序
        doctor_details.sort(key=lambda x: x["appointment_count"], reverse=True)
        
        # 统计就诊原因
        reason_stats = Counter()
        for appointment in valid_appointments:
            reason_stats[appointment.reason] += 1
        
        reason_details = []
        for reason, count in reason_stats.items():
            reason_details.append({
                "reason": reason,
                "count": count
            })
        
        # 高峰时间分析
        time_slot_stats = Counter()
        for appointment in valid_appointments:
            time_slot_stats[appointment.time_slot] += 1
        
        # 找出预约量最大的3个时间槽
        peak_times = []
        for time_slot, count in time_slot_stats.most_common(3):
            peak_times.append({
                "time_slot": time_slot,
                "time_display": self._get_time_slot_display(time_slot),
                "count": count
            })
        
        # 整合报告数据
        report_data = {
            "clinic_id": clinic_id,
            "clinic_name": clinic.name,
            "date_range": f"{start_date} 至 {end_date}",
            "total_appointments": total_appointments,
            "doctor_stats": doctor_details,
            "reason_stats": reason_details,
            "peak_times": peak_times
        }
        
        return report_data
    
    def generate_appointment_type_report(self, date_range_type: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """生成预约类型分布报告
        
        Args:
            date_range_type (str): 日期范围类型，可选值：'day', 'week', 'month', 'custom'
            start_date (str, optional): 自定义范围起始日期，格式为 "YYYY-MM-DD"
            end_date (str, optional): 自定义范围结束日期，格式为 "YYYY-MM-DD"
            
        Returns:
            Dict[str, Any]: 预约类型分布报告数据
        """
        # 获取日期范围
        start_date, end_date = self._get_date_range(date_range_type, start_date, end_date)
        
        # 获取所有预约
        all_appointments = self.__appointment_repo.get_all()
        
        # 按日期范围筛选预约
        filtered_appointments = self._filter_appointments_by_date_range(all_appointments, start_date, end_date)
        
        # 有效预约（已完成或已安排）
        valid_appointments = [app for app in filtered_appointments 
                             if app.is_completed() or app.is_scheduled()]
        
        # 统计总预约数
        total_appointments = len(valid_appointments)
        
        if total_appointments == 0:
            return {
                "date_range": f"{start_date} 至 {end_date}",
                "total_appointments": 0,
                "type_stats": []
            }
        
        # 统计预约类型分布
        reason_stats = Counter()
        for appointment in valid_appointments:
            reason_stats[appointment.reason] += 1
        
        # 计算百分比
        type_stats = []
        for reason, count in reason_stats.items():
            percentage = (count / total_appointments) * 100
            type_stats.append({
                "reason": reason,
                "count": count,
                "percentage": round(percentage, 2)
            })
        
        # 按数量降序排序
        type_stats.sort(key=lambda x: x["count"], reverse=True)
        
        # 整合报告数据
        report_data = {
            "date_range": f"{start_date} 至 {end_date}",
            "total_appointments": total_appointments,
            "type_stats": type_stats
        }
        
        return report_data
    
    def export_report_to_csv(self, report_data: Any, report_type: str, filename: str = None) -> str:
        """将报告导出为CSV文件
        
        Args:
            report_data (Any): 报告数据
            report_type (str): 报告类型，可选值：'doctor', 'clinic', 'appointment_type'
            filename (str, optional): 自定义文件名
            
        Returns:
            str: CSV文件路径
        """
        # 创建导出目录
        export_dir = os.path.join("exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # 生成默认文件名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_type}_report_{timestamp}.csv"
        
        # 确保文件扩展名为.csv
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        file_path = os.path.join(export_dir, filename)
        
        # 根据报告类型写入不同的CSV格式
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            if report_type == 'doctor':
                # 医生报告
                fieldnames = ['doctor_id', 'doctor_name', 'clinic_suburbs', 'appointment_count', 'appointment_reasons']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in report_data:
                    writer.writerow(item)
            
            elif report_type == 'clinic':
                # 诊所报告
                writer = csv.writer(csvfile)
                
                # 写入基本信息
                writer.writerow(['诊所ID', '诊所名称', '日期范围', '总预约数'])
                writer.writerow([
                    report_data['clinic_id'],
                    report_data['clinic_name'],
                    report_data['date_range'],
                    report_data['total_appointments']
                ])
                
                # 写入医生统计信息
                writer.writerow([])
                writer.writerow(['医生ID', '医生姓名', '预约数量'])
                for doctor in report_data['doctor_stats']:
                    writer.writerow([
                        doctor['doctor_id'],
                        doctor['doctor_name'],
                        doctor['appointment_count']
                    ])
                
                # 写入预约原因统计
                writer.writerow([])
                writer.writerow(['预约原因', '数量'])
                for reason in report_data['reason_stats']:
                    writer.writerow([reason['reason'], reason['count']])
                
                # 写入高峰时间分析
                writer.writerow([])
                writer.writerow(['时间段', '预约数量'])
                for peak in report_data['peak_times']:
                    writer.writerow([peak['time_display'], peak['count']])
            
            elif report_type == 'appointment_type':
                # 预约类型分布报告
                writer = csv.writer(csvfile)
                
                # 写入基本信息
                writer.writerow(['日期范围', report_data['date_range']])
                writer.writerow(['总预约数', report_data['total_appointments']])
                
                # 写入类型统计
                writer.writerow([])
                writer.writerow(['预约原因', '数量', '百分比'])
                for type_stat in report_data['type_stats']:
                    writer.writerow([
                        type_stat['reason'], 
                        type_stat['count'],
                        f"{type_stat['percentage']}%"
                    ])
        
        return file_path
    
    def export_report_to_txt(self, report_data: Any, report_type: str, filename: str = None) -> str:
        """将报告导出为TXT文件
        
        Args:
            report_data (Any): 报告数据
            report_type (str): 报告类型，可选值：'doctor', 'clinic', 'appointment_type'
            filename (str, optional): 自定义文件名
            
        Returns:
            str: TXT文件路径
        """
        # 创建导出目录
        export_dir = os.path.join("exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # 生成默认文件名
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_type}_report_{timestamp}.txt"
        
        # 确保文件扩展名为.txt
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        file_path = os.path.join(export_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as txtfile:
            if report_type == 'doctor':
                # 医生报告
                txtfile.write("=====================================================\n")
                txtfile.write("              医生接待人数统计报告                  \n")
                txtfile.write("=====================================================\n\n")
                
                for item in report_data:
                    txtfile.write(f"医生ID: {item['doctor_id']}\n")
                    txtfile.write(f"医生姓名: {item['doctor_name']}\n")
                    txtfile.write(f"所在诊所区域: {item['clinic_suburbs']}\n")
                    txtfile.write(f"接待人数: {item['appointment_count']}\n")
                    txtfile.write(f"就诊原因: {item['appointment_reasons']}\n")
                    txtfile.write("-" * 50 + "\n")
            
            elif report_type == 'clinic':
                # 诊所报告
                txtfile.write("=====================================================\n")
                txtfile.write("              诊所预约数据统计报告                  \n")
                txtfile.write("=====================================================\n\n")
                
                txtfile.write(f"诊所ID: {report_data['clinic_id']}\n")
                txtfile.write(f"诊所名称: {report_data['clinic_name']}\n")
                txtfile.write(f"日期范围: {report_data['date_range']}\n")
                txtfile.write(f"总预约数: {report_data['total_appointments']}\n\n")
                
                txtfile.write("医生预约统计:\n")
                txtfile.write("-" * 50 + "\n")
                for doctor in report_data['doctor_stats']:
                    txtfile.write(f"医生: {doctor['doctor_name']} (ID: {doctor['doctor_id']}), 预约数: {doctor['appointment_count']}\n")
                
                txtfile.write("\n就诊原因统计:\n")
                txtfile.write("-" * 50 + "\n")
                for reason in report_data['reason_stats']:
                    txtfile.write(f"{reason['reason']}: {reason['count']}\n")
                
                txtfile.write("\n高峰时间分析:\n")
                txtfile.write("-" * 50 + "\n")
                for peak in report_data['peak_times']:
                    txtfile.write(f"{peak['time_display']}: {peak['count']} 预约\n")
            
            elif report_type == 'appointment_type':
                # 预约类型分布报告
                txtfile.write("=====================================================\n")
                txtfile.write("              预约类型分布统计报告                  \n")
                txtfile.write("=====================================================\n\n")
                
                txtfile.write(f"日期范围: {report_data['date_range']}\n")
                txtfile.write(f"总预约数: {report_data['total_appointments']}\n\n")
                
                txtfile.write("预约类型分布:\n")
                txtfile.write("-" * 50 + "\n")
                for type_stat in report_data['type_stats']:
                    txtfile.write(f"{type_stat['reason']}: {type_stat['count']} ({type_stat['percentage']}%)\n")
        
        return file_path 