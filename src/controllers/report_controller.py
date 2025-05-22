#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
报告控制器类 - 处理报告统计UI界面和交互
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime

from src.entities.user import User
from src.services.report_service import ReportService
from src.repositories.clinic_repository import ClinicRepository

class ReportController:
    """报告控制器类"""
    
    def __init__(self, user=None):
        """初始化报告控制器
        
        Args:
            user (User, optional): 当前用户. Defaults to None.
        """
        self.__report_svc = ReportService()
        self.__clinic_repo = ClinicRepository()
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
        print("=" * 50)
        print()
    
    def wait_for_key(self):
        """等待用户按键"""
        input("\n按回车键继续...")
    
    def _select_date_range(self) -> tuple:
        """选择日期范围
        
        Returns:
            tuple: (日期范围类型, 开始日期, 结束日期)
        """
        self.print_header("选择日期范围")
        print("1. 今天")
        print("2. 本周（过去7天）")
        print("3. 本月（过去30天）")
        print("4. 自定义范围")
        print("0. 返回")
        
        choice = input("\n请选择: ").strip()
        
        if choice == "0":
            return None, None, None
        
        range_type = None
        start_date = None
        end_date = None
        
        if choice == "1":
            range_type = "day"
        elif choice == "2":
            range_type = "week"
        elif choice == "3":
            range_type = "month"
        elif choice == "4":
            print("\n请输入自定义日期范围（格式：YYYY-MM-DD）")
            start_date = input("开始日期: ").strip()
            end_date = input("结束日期: ").strip()
            
            # 验证日期格式
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
                range_type = "custom"
            except ValueError:
                print("日期格式无效，请使用 YYYY-MM-DD 格式")
                self.wait_for_key()
                return self._select_date_range()
        else:
            print("无效选择")
            self.wait_for_key()
            return self._select_date_range()
        
        return range_type, start_date, end_date
    
    def _select_export_format(self) -> str:
        """选择导出格式
        
        Returns:
            str: 导出格式，可选值：'csv', 'txt', None表示取消导出
        """
        print("\n请选择导出格式:")
        print("1. CSV格式")
        print("2. TXT格式")
        print("0. 不导出")
        
        choice = input("\n请选择: ").strip()
        
        if choice == "0":
            return None
        elif choice == "1":
            return "csv"
        elif choice == "2":
            return "txt"
        else:
            print("无效选择")
            return self._select_export_format()
    
    def _export_report(self, report_data: Any, report_type: str) -> None:
        """导出报告
        
        Args:
            report_data (Any): 报告数据
            report_type (str): 报告类型
        """
        if not report_data:
            print("没有可导出的报告数据")
            return
        
        export_format = self._select_export_format()
        if not export_format:
            return
        
        filename = input("\n请输入文件名（默认自动生成）: ").strip()
        
        if export_format == "csv":
            file_path = self.__report_svc.export_report_to_csv(report_data, report_type, filename)
        else:
            file_path = self.__report_svc.export_report_to_txt(report_data, report_type, filename)
        
        print(f"\n报告已导出到: {file_path}")
    
    def show_doctor_report(self) -> None:
        """显示医生接待人数报告"""
        self.print_header("医生接待人数报告")
        
        # 选择日期范围
        range_type, start_date, end_date = self._select_date_range()
        if not range_type:
            return
        
        # 生成报告
        report_data = self.__report_svc.generate_doctor_report(range_type, start_date, end_date)
        
        if not report_data:
            print("没有找到符合条件的数据")
            self.wait_for_key()
            return
        
        # 显示报告
        self.print_header("医生接待人数统计报告")
        start, end = self.__report_svc._get_date_range(range_type, start_date, end_date)
        print(f"日期范围: {start} 至 {end}")
        print(f"总记录数: {len(report_data)}")
        print()
        
        print(f"{'医生ID':<8}{'医生姓名':<15}{'所在诊所区域':<20}{'接待人数':<10}{'就诊原因'}")
        print("-" * 80)
        
        for item in report_data:
            print(f"{item['doctor_id']:<8}{item['doctor_name']:<15}{item['clinic_suburbs']:<20}{item['appointment_count']:<10}{item['appointment_reasons']}")
        
        # 导出选项
        print("\n请选择操作:")
        print("1. 导出报告")
        print("0. 返回")
        
        choice = input("\n请选择: ").strip()
        
        if choice == "1":
            self._export_report(report_data, "doctor")
        
        self.wait_for_key()
    
    def show_clinic_report(self) -> None:
        """显示诊所预约数据报告"""
        self.print_header("诊所预约数据报告")
        
        # 选择诊所
        clinics = self.__clinic_repo.get_all()
        if not clinics:
            print("系统中没有诊所数据")
            self.wait_for_key()
            return
        
        print("请选择诊所:")
        for i, clinic in enumerate(clinics, 1):
            print(f"{i}. {clinic.name} ({clinic.suburb})")
        print("0. 返回")
        
        choice = input("\n请选择: ").strip()
        
        if choice == "0":
            return
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(clinics):
                selected_clinic = clinics[idx]
            else:
                print("无效选择")
                self.wait_for_key()
                return
        except ValueError:
            print("请输入有效的数字")
            self.wait_for_key()
            return
        
        # 选择日期范围
        range_type, start_date, end_date = self._select_date_range()
        if not range_type:
            return
        
        # 生成报告
        report_data = self.__report_svc.generate_clinic_report(selected_clinic.id, range_type, start_date, end_date)
        
        if "error" in report_data:
            print(f"错误: {report_data['error']}")
            self.wait_for_key()
            return
        
        # 显示报告
        self.print_header("诊所预约数据统计报告")
        print(f"诊所: {report_data['clinic_name']}")
        print(f"日期范围: {report_data['date_range']}")
        print(f"总预约数: {report_data['total_appointments']}")
        
        # 医生预约统计
        print("\n医生预约统计:")
        print("-" * 50)
        print(f"{'医生ID':<8}{'医生姓名':<15}{'预约数量'}")
        print("-" * 50)
        
        for doctor in report_data['doctor_stats']:
            print(f"{doctor['doctor_id']:<8}{doctor['doctor_name']:<15}{doctor['appointment_count']}")
        
        # 就诊原因统计
        print("\n就诊原因统计:")
        print("-" * 50)
        print(f"{'就诊原因':<30}{'数量'}")
        print("-" * 50)
        
        for reason in report_data['reason_stats']:
            print(f"{reason['reason']:<30}{reason['count']}")
        
        # 高峰时间分析
        print("\n高峰时间分析:")
        print("-" * 50)
        print(f"{'时间段':<20}{'预约数量'}")
        print("-" * 50)
        
        for peak in report_data['peak_times']:
            print(f"{peak['time_display']:<20}{peak['count']}")
        
        # 导出选项
        print("\n请选择操作:")
        print("1. 导出报告")
        print("0. 返回")
        
        choice = input("\n请选择: ").strip()
        
        if choice == "1":
            self._export_report(report_data, "clinic")
        
        self.wait_for_key()
    
    def show_appointment_type_report(self) -> None:
        """显示预约类型分布报告"""
        self.print_header("预约类型分布报告")
        
        # 选择日期范围
        range_type, start_date, end_date = self._select_date_range()
        if not range_type:
            return
        
        # 生成报告
        report_data = self.__report_svc.generate_appointment_type_report(range_type, start_date, end_date)
        
        # 显示报告
        self.print_header("预约类型分布统计报告")
        print(f"日期范围: {report_data['date_range']}")
        print(f"总预约数: {report_data['total_appointments']}")
        
        if report_data['total_appointments'] == 0:
            print("\n所选时间范围内没有预约数据")
            self.wait_for_key()
            return
        
        print("\n预约类型分布:")
        print("-" * 70)
        print(f"{'预约原因':<40}{'数量':<10}{'百分比'}")
        print("-" * 70)
        
        for type_stat in report_data['type_stats']:
            print(f"{type_stat['reason']:<40}{type_stat['count']:<10}{type_stat['percentage']}%")
        
        # 导出选项
        print("\n请选择操作:")
        print("1. 导出报告")
        print("0. 返回")
        
        choice = input("\n请选择: ").strip()
        
        if choice == "1":
            self._export_report(report_data, "appointment_type")
        
        self.wait_for_key()
    
    def run(self) -> bool:
        """运行报告统计菜单
        
        Returns:
            bool: 是否返回主菜单
        """
        self.__should_return_to_main = False  # 重置返回主菜单标志
        
        while True:
            if self.__should_return_to_main:
                break
                
            self.print_header("统计报告管理")
            
            print("1. 医生接待人数报告")
            print("2. 诊所预约数据报告")
            print("3. 预约类型分布报告")
            print("0. 返回上一级")
            print("-. 返回主菜单")
            
            choice = input("\n请选择操作: ").strip()
            
            if choice == "1":
                self.show_doctor_report()
            elif choice == "2":
                self.show_clinic_report()
            elif choice == "3":
                self.show_appointment_type_report()
            elif choice == "0":
                break
            elif choice == "-":
                self.__should_return_to_main = True
                break
            else:
                print("无效选项")
                self.wait_for_key()
        
        return self.__should_return_to_main 