#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Report Controller - Handles report and statistics UI and interactions
"""

import os
from typing import Optional, Dict, Any, List
from datetime import datetime

from src.entities.user import User
from src.services.report_service import ReportService
from src.repositories.clinic_repository import ClinicRepository
from src.repositories.doctor_repository import DoctorRepository

class ReportController:
    """Report Controller"""
    
    def __init__(self, user=None):
        """Initialize report controller
        
        Args:
            user (User, optional): Current user. Defaults to None.
        """
        self.__report_svc = ReportService()
        self.__clinic_repo = ClinicRepository()
        self.__doctor_repo = DoctorRepository()
        self.__current_user = user
        self.__should_return_to_main = False  # Flag to return to main menu
    
    def clear_screen(self):
        """Clear screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print title header
        
        Args:
            title (str): The title to display
        """
        self.clear_screen()
        print("=" * 50)
        print(f"{title.center(48)}")
        print("=" * 50)
        print()
    
    def wait_for_key(self):
        """Wait for user to press a key"""
        input("\nPress Enter to continue...")
    
    def _select_date_range(self) -> tuple:
        """Select date range
        
        Returns:
            tuple: (range_type, start_date, end_date) where range_type is one of 'day', 'week', 'month', 'custom'
                  or (None, None, None) if canceled
        """
        self.print_header("Select Date Range")
        print("1. Today")
        print("2. This Week (last 7 days)")
        print("3. This Month (last 30 days)")
        print("4. Custom Range")
        print("0. Return")
        
        choice = input("\nSelect: ").strip()
        
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
            print("\nEnter custom date range (format: YYYY-MM-DD)")
            start_date = input("Start date: ").strip()
            end_date = input("End date: ").strip()
            
            # Validate date format
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                datetime.strptime(end_date, "%Y-%m-%d")
                range_type = "custom"
            except ValueError:
                print("Invalid date format, please use YYYY-MM-DD format")
                self.wait_for_key()
                return self._select_date_range()
        else:
            print("Invalid choice")
            self.wait_for_key()
            return self._select_date_range()
        
        return range_type, start_date, end_date
    
    def _select_export_format(self) -> str:
        """Select export format
        
        Returns:
            str: Export format, possible values: 'csv', 'txt', None if export canceled
        """
        print("\nSelect export format:")
        print("1. CSV format")
        print("2. TXT format")
        print("0. Don't export")
        
        choice = input("\nSelect: ").strip()
        
        if choice == "0":
            return None
        elif choice == "1":
            return "csv"
        elif choice == "2":
            return "txt"
        else:
            print("Invalid choice")
            return self._select_export_format()
    
    def _export_report(self, report_data: Any, report_type: str) -> None:
        """Export report
        
        Args:
            report_data (Any): Report data
            report_type (str): Report type
        """
        if not report_data:
            print("No report data to export")
            return
        
        export_format = self._select_export_format()
        if not export_format:
            return
        
        filename = input("\nEnter filename (default: auto-generated): ").strip()
        
        if export_format == "csv":
            file_path = self.__report_svc.export_report_to_csv(report_data, report_type, filename)
        else:
            file_path = self.__report_svc.export_report_to_txt(report_data, report_type, filename)
        
        print(f"\nReport exported to: {file_path}")
    
    def show_doctor_report(self) -> None:
        """Display doctor patient statistics report"""
        self.print_header("Doctor Patient Statistics Report")
        
        # Select date range
        range_type, start_date, end_date = self._select_date_range()
        if not range_type:
            return
        
        # Generate report
        report_data = self.__report_svc.generate_doctor_report(range_type, start_date, end_date)
        
        if not report_data:
            print("No data found matching the criteria")
            self.wait_for_key()
            return
        
        # Display report
        self.print_header("Doctor Patient Statistics Report")
        start, end = self.__report_svc._get_date_range(range_type, start_date, end_date)
        print(f"Date range: {start} to {end}")
        print(f"Total records: {len(report_data)}")
        print()
        
        print(f"{'Doctor ID':<8}{'Doctor Name':<15}{'Clinic Suburbs':<20}{'Patient Count':<10}{'Appointment Reasons'}")
        print("-" * 80)
        
        for item in report_data:
            print(f"{item['doctor_id']:<8}{item['doctor_name']:<15}{item['clinic_suburbs']:<20}{item['appointment_count']:<10}{item['appointment_reasons']}")
        
        # Export options
        print("\nSelect an option:")
        print("1. Export Report")
        print("0. Return")
        
        choice = input("\nSelect: ").strip()
        
        if choice == "1":
            self._export_report(report_data, "doctor")
        
        self.wait_for_key()
    
    def show_clinic_report(self) -> None:
        """Display clinic appointment data report"""
        self.print_header("Clinic Appointment Data Report")
        
        # Select clinic
        clinics = self.__clinic_repo.get_all()
        if not clinics:
            print("No clinic data in the system")
            self.wait_for_key()
            return
        
        print("Select clinic:")
        for i, clinic in enumerate(clinics, 1):
            print(f"{i}. {clinic.name} ({clinic.suburb})")
        print("0. Return")
        
        choice = input("\nSelect: ").strip()
        
        if choice == "0":
            return
        
        try:
            clinic_idx = int(choice) - 1
            if clinic_idx < 0 or clinic_idx >= len(clinics):
                raise ValueError("Invalid index")
            
            selected_clinic = clinics[clinic_idx]
            
            # Select date range
            range_type, start_date, end_date = self._select_date_range()
            if not range_type:
                return
            
            # Generate report
            report_data = self.__report_svc.generate_clinic_report(selected_clinic.id, range_type, start_date, end_date)
            
            if not report_data:
                print("No data found matching the criteria")
                self.wait_for_key()
                return
            
            # Check for error
            if 'error' in report_data:
                print(f"Error: {report_data['error']}")
                self.wait_for_key()
                return
            
            # Display report
            self.print_header(f"Clinic Report: {selected_clinic.name}")
            print(f"Date range: {report_data['date_range']}")
            print(f"Total appointments: {report_data['total_appointments']}")
            print()
            
            # Peak time analysis
            print("Appointment Distribution by Hour:")
            if 'hour_distribution' in report_data and report_data['hour_distribution']:
                max_count = max(report_data['hour_distribution'].values()) if report_data['hour_distribution'] else 0
                
                for hour in sorted(report_data['hour_distribution'].keys()):
                    count = report_data['hour_distribution'][hour]
                    bar_length = int((count / max_count) * 20) if max_count > 0 else 0
                    is_peak = hour in report_data['peak_hours'] if 'peak_hours' in report_data else False
                    hour_display = f"{hour}:00-{hour+1}:00"
                    peak_marker = " (PEAK)" if is_peak else ""
                    
                    print(f"{hour_display:<10} {count:>3} {'█' * bar_length}{peak_marker}")
            else:
                print("No hour distribution data available")
            
            print("\nDoctor Appointment Distribution:")
            if 'doctor_distribution' in report_data:
                for doctor_id, count in report_data['doctor_distribution'].items():
                    doctor_name = "Unknown"
                    doctor = self.__doctor_repo.get_by_id(doctor_id)
                    if doctor:
                        doctor_name = doctor.full_name
                    print(f"{doctor_name:<20}: {count} appointments")
            else:
                print("No doctor distribution data available")
            
            # Export options
            print("\nSelect an option:")
            print("1. Export Report")
            print("0. Return")
            
            choice = input("\nSelect: ").strip()
            
            if choice == "1":
                self._export_report(report_data, "clinic")
            
        except (ValueError, IndexError) as e:
            print(f"Invalid selection: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        self.wait_for_key()
    
    def show_appointment_type_report(self) -> None:
        """Display appointment type distribution report"""
        self.print_header("Appointment Type Distribution Report")
        
        # Select date range
        range_type, start_date, end_date = self._select_date_range()
        if not range_type:
            return
        
        # Generate report
        report_data = self.__report_svc.generate_appointment_type_report(range_type, start_date, end_date)
        
        if not report_data:
            print("No data found matching the criteria")
            self.wait_for_key()
            return
        
        # Display report
        self.print_header("Appointment Type Distribution Report")
        start, end = self.__report_svc._get_date_range(range_type, start_date, end_date)
        print(f"Date range: {start} to {end}")
        print(f"Total appointments: {sum(report_data.values())}")
        print()
        
        max_count = max(report_data.values()) if report_data else 0
        
        for reason, count in sorted(report_data.items(), key=lambda x: x[1], reverse=True):
            bar_length = int((count / max_count) * 30) if max_count > 0 else 0
            percentage = (count / sum(report_data.values())) * 100 if sum(report_data.values()) > 0 else 0
            
            print(f"{reason:<20} {count:>4} ({percentage:.1f}%) {'█' * bar_length}")
        
        # Export options
        print("\nSelect an option:")
        print("1. Export Report")
        print("0. Return")
        
        choice = input("\nSelect: ").strip()
        
        if choice == "1":
            self._export_report(report_data, "appointment_type")
        
        self.wait_for_key()
    
    def run(self) -> bool:
        """Run report menu
        
        Returns:
            bool: Flag indicating whether to return to main menu
        """
        self.__should_return_to_main = False  # Reset return to main menu flag
        
        while True:
            if self.__should_return_to_main:
                break
                
            self.print_header("Reports and Statistics")
            
            print("1. Doctor Patient Statistics")
            print("2. Clinic Appointment Data")
            print("3. Appointment Type Distribution")
            print("0. Return")
            print("-. Back to Main Menu")
            
            choice = input("\nSelect: ").strip()
            
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
                print("Invalid option")
                self.wait_for_key()
        
        return self.__should_return_to_main  # Return flag, for caller to determine if returning to main menu 