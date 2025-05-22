#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Report Service - Handles business logic for statistical reports
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
    """Report Service"""
    
    def __init__(self):
        """Initialize report service"""
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
        """Generate clinic appointment data report
        
        Args:
            clinic_id (int): Clinic ID
            date_range_type (str): Date range type, options: 'day', 'week', 'month', 'custom'
            start_date (str, optional): Custom range start date in format "YYYY-MM-DD"
            end_date (str, optional): Custom range end date in format "YYYY-MM-DD"
            
        Returns:
            Dict[str, Any]: Clinic report data
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
        doctor_distribution = defaultdict(int)
        for appointment in valid_appointments:
            doctor_distribution[appointment.doctor_id] += 1
        
        # 获取医生详细信息
        doctor_details = []
        for doctor_id, count in doctor_distribution.items():
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
            # Convert time slot (0-15) to hour (9-18)
            # Time slots 0-5 correspond to 9:00-12:00 (morning hours 9-12)
            # Time slots 6-15 correspond to 13:00-18:00 (afternoon hours 13-18)
            hour = 9 + (appointment.time_slot // 2)
            if appointment.time_slot > 5:  # Afternoon slots start at index 6
                hour += 1  # Skip lunch hour (12-13)
            time_slot_stats[hour] += 1
        
        # Find the top 3 peak hours
        peak_hours = [hour for hour, _ in time_slot_stats.most_common(3)]
        
        # Create hour distribution data
        hour_distribution = {}
        for hour in range(9, 19):  # 9:00 to 18:00
            hour_distribution[hour] = time_slot_stats[hour]
        
        # Find top 3 peak time slots
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
            "date_range": f"{start_date} to {end_date}",
            "total_appointments": total_appointments,
            "doctor_distribution": doctor_distribution,
            "doctor_stats": doctor_details,
            "reason_stats": reason_details,
            "peak_times": peak_times,
            "hour_distribution": hour_distribution,
            "peak_hours": peak_hours
        }
        
        return report_data
    
    def generate_appointment_type_report(self, date_range_type: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Generate appointment type distribution report
        
        Args:
            date_range_type (str): Date range type, options: 'day', 'week', 'month', 'custom'
            start_date (str, optional): Custom range start date in format "YYYY-MM-DD"
            end_date (str, optional): Custom range end date in format "YYYY-MM-DD"
            
        Returns:
            Dict[str, Any]: Appointment type distribution report data
        """
        # Get date range
        start_date, end_date = self._get_date_range(date_range_type, start_date, end_date)
        
        # Get all appointments
        all_appointments = self.__appointment_repo.get_all()
        
        # Filter appointments by date range
        filtered_appointments = self._filter_appointments_by_date_range(all_appointments, start_date, end_date)
        
        # Valid appointments (completed or scheduled)
        valid_appointments = [app for app in filtered_appointments 
                             if app.is_completed() or app.is_scheduled()]
        
        # Count total appointments
        total_appointments = len(valid_appointments)
        
        if total_appointments == 0:
            return {
                "date_range": f"{start_date} to {end_date}",
                "total_appointments": 0,
                "type_stats": [],
                "reason_counts": {}  # Add an empty reason_counts dictionary
            }
        
        # Count appointments by reason
        reason_stats = Counter()
        for appointment in valid_appointments:
            reason_stats[appointment.reason] += 1
        
        # Calculate percentages
        type_stats = []
        for reason, count in reason_stats.items():
            percentage = (count / total_appointments) * 100
            type_stats.append({
                "reason": reason,
                "count": count,
                "percentage": round(percentage, 2)
            })
        
        # Sort by count in descending order
        type_stats.sort(key=lambda x: x["count"], reverse=True)
        
        # Create a simplified reason_counts dictionary for direct use
        reason_counts = {}
        for reason, count in reason_stats.items():
            reason_counts[reason] = count
        
        # Integrate report data
        report_data = {
            "date_range": f"{start_date} to {end_date}",
            "total_appointments": total_appointments,
            "type_stats": type_stats,
            "reason_counts": reason_counts  # Add the reason_counts dictionary
        }
        
        return report_data
    
    def export_report_to_csv(self, report_data: Any, report_type: str, filename: str = None) -> str:
        """Export report to CSV file
        
        Args:
            report_data (Any): Report data
            report_type (str): Report type, options: 'doctor', 'clinic', 'appointment_type'
            filename (str, optional): Custom filename
            
        Returns:
            str: CSV file path
        """
        # Create export directory
        export_dir = os.path.join("exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Generate default filename
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_type}_report_{timestamp}.csv"
        
        # Ensure file extension is .csv
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        file_path = os.path.join(export_dir, filename)
        
        # Write different CSV formats based on report type
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            if report_type == 'doctor':
                # Doctor report
                fieldnames = ['doctor_id', 'doctor_name', 'clinic_suburbs', 'appointment_count', 'appointment_reasons']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in report_data:
                    writer.writerow(item)
            
            elif report_type == 'clinic':
                # Clinic report
                writer = csv.writer(csvfile)
                
                # Write basic information
                writer.writerow(['Clinic ID', 'Clinic Name', 'Date Range', 'Total Appointments'])
                writer.writerow([
                    report_data['clinic_id'],
                    report_data['clinic_name'],
                    report_data['date_range'],
                    report_data['total_appointments']
                ])
                
                # Write doctor statistics
                writer.writerow([])
                writer.writerow(['Doctor ID', 'Doctor Name', 'Appointment Count'])
                for doctor in report_data['doctor_stats']:
                    writer.writerow([
                        doctor['doctor_id'],
                        doctor['doctor_name'],
                        doctor['appointment_count']
                    ])
                
                # Write reason statistics
                writer.writerow([])
                writer.writerow(['Reason', 'Count'])
                for reason in report_data['reason_stats']:
                    writer.writerow([reason['reason'], reason['count']])
                
                # Write peak time analysis
                writer.writerow([])
                writer.writerow(['Time Slot', 'Appointment Count'])
                for peak in report_data['peak_times']:
                    writer.writerow([peak['time_display'], peak['count']])
            
            elif report_type == 'appointment_type':
                # Appointment type distribution report
                writer = csv.writer(csvfile)
                
                # Write basic information
                writer.writerow(['Date Range', report_data['date_range']])
                writer.writerow(['Total Appointments', report_data['total_appointments']])
                
                # Write type statistics
                writer.writerow([])
                writer.writerow(['Reason', 'Count', 'Percentage'])
                
                if 'type_stats' in report_data:
                    for type_stat in report_data['type_stats']:
                        writer.writerow([
                            type_stat['reason'], 
                            type_stat['count'],
                            f"{type_stat['percentage']}%"
                        ])
        
        return file_path
    
    def export_report_to_txt(self, report_data: Any, report_type: str, filename: str = None) -> str:
        """Export report to TXT file
        
        Args:
            report_data (Any): Report data
            report_type (str): Report type, options: 'doctor', 'clinic', 'appointment_type'
            filename (str, optional): Custom filename
            
        Returns:
            str: TXT file path
        """
        # Create export directory
        export_dir = os.path.join("exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Generate default filename
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_type}_report_{timestamp}.txt"
        
        # Ensure file extension is .txt
        if not filename.endswith('.txt'):
            filename += '.txt'
        
        file_path = os.path.join(export_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as txtfile:
            if report_type == 'doctor':
                # Doctor report
                txtfile.write("=====================================================\n")
                txtfile.write("              Doctor Patient Statistics Report       \n")
                txtfile.write("=====================================================\n\n")
                
                for item in report_data:
                    txtfile.write(f"Doctor ID: {item['doctor_id']}\n")
                    txtfile.write(f"Doctor Name: {item['doctor_name']}\n")
                    txtfile.write(f"Clinic Suburbs: {item['clinic_suburbs']}\n")
                    txtfile.write(f"Appointment Count: {item['appointment_count']}\n")
                    txtfile.write(f"Appointment Reasons: {item['appointment_reasons']}\n")
                    txtfile.write("-" * 50 + "\n")
            
            elif report_type == 'clinic':
                # Clinic report
                txtfile.write("=====================================================\n")
                txtfile.write("              Clinic Appointment Data Report         \n")
                txtfile.write("=====================================================\n\n")
                
                txtfile.write(f"Clinic ID: {report_data['clinic_id']}\n")
                txtfile.write(f"Clinic Name: {report_data['clinic_name']}\n")
                txtfile.write(f"Date Range: {report_data['date_range']}\n")
                txtfile.write(f"Total Appointments: {report_data['total_appointments']}\n\n")
                
                txtfile.write("Doctor Appointment Distribution:\n")
                txtfile.write("-" * 50 + "\n")
                for doctor in report_data['doctor_stats']:
                    txtfile.write(f"Doctor: {doctor['doctor_name']} (ID: {doctor['doctor_id']}), Appointments: {doctor['appointment_count']}\n")
                
                txtfile.write("\nReason Statistics:\n")
                txtfile.write("-" * 50 + "\n")
                for reason in report_data['reason_stats']:
                    txtfile.write(f"{reason['reason']}: {reason['count']}\n")
                
                txtfile.write("\nPeak Time Analysis:\n")
                txtfile.write("-" * 50 + "\n")
                for peak in report_data['peak_times']:
                    txtfile.write(f"{peak['time_display']}: {peak['count']} appointments\n")
            
            elif report_type == 'appointment_type':
                # Appointment type distribution report
                txtfile.write("=====================================================\n")
                txtfile.write("          Appointment Type Distribution Report       \n")
                txtfile.write("=====================================================\n\n")
                
                txtfile.write(f"Date Range: {report_data['date_range']}\n")
                txtfile.write(f"Total Appointments: {report_data['total_appointments']}\n\n")
                
                txtfile.write("Appointment Type Distribution:\n")
                txtfile.write("-" * 50 + "\n")
                
                if 'type_stats' in report_data:
                    for type_stat in report_data['type_stats']:
                        txtfile.write(f"{type_stat['reason']}: {type_stat['count']} ({type_stat['percentage']}%)\n")
        
        return file_path 