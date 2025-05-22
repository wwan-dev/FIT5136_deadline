#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Appointment Controller - Handles appointment-related UI and interactions
"""

import os
from typing import Optional, Dict, Any, Tuple, List

from src.entities.user import User
from src.services.appointment_service import AppointmentService
from src.utils.date_util import DateUtil

class AppointmentController:
    """Appointment Controller - Handles appointment-related UI and interactions"""
    
    def __init__(self, user=None):
        """Initialize appointment controller
        
        Args:
            user (User, optional): Current user. Defaults to None.
        """
        self.__appointment_service = AppointmentService()
        self.__current_user = user
        self.__should_return_to_main = False  # Flag to return to main menu
        self.__DateUtil = DateUtil()
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
        print()
    
    def wait_for_key(self):
        """Wait for user to press a key"""
        input("\nPress Enter to continue...")
    
    def print_navigation_options(self, has_default=True, default_text=""):
        """Print navigation options
        
        Args:
            has_default (bool): Whether to show default option
            default_text (str): Text for default option
        """
        print("\n0. Return")
        print("-. Back to Main Menu")
        if has_default and default_text:
            print(f"Press Enter to {default_text}")
    
    def handle_navigation_choice(self, choice: str) -> int:
        """Handle navigation choice
        
        Args:
            choice (str): User input
            
        Returns:
            int: 0 means return to previous menu, -1 means return to main menu, other values are actual selections
        """
        if choice == "-":
            self.__should_return_to_main = True
            return -1
        return 0 if choice == "0" else 1
    
    def get_clinic_selection(self, default_option: bool = True) -> Optional[int]:
        """Display clinic selection interface
        
        Args:
            default_option (bool): Whether to show default option (all clinics)
            
        Returns:
            Optional[int]: Selected clinic ID, returns None if all clinics selected
                          Returns -1 to go back, if self.__should_return_to_main is True then return to main menu
        """
        self.print_header("Select Clinic")
        
        clinics = self.__appointment_service.get_all_clinics()
        
        if not clinics:
            print("No clinic records found")
            self.wait_for_key()
            return -1
        
        print(f"{'ID':<5}{'Name':<15}{'Suburb':<10}{'Address':<20}{'Phone':<15}")
        print("-" * 65)
        
        for clinic in clinics:
            print(f"{clinic.id:<5}{clinic.name:<15}{clinic.suburb:<10}{clinic.address:<20}{clinic.phone:<15}")
        
        option_text = "\nSelect clinic ID"
        if default_option:
            option_text += ", or enter 0 to view all clinics/return"
        else:
            option_text += ", or enter 0 to return"
        option_text += ", enter - to return to main menu"
        option_text += ", press Enter to view all clinics by default: "
        
        print(option_text, end="")
        choice = input()
        
        if choice == "":
            return None  # Press Enter to view all clinics by default
        
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
                print("Invalid clinic ID")
                self.wait_for_key()
                return self.get_clinic_selection(default_option)
        except ValueError:
            print("Please enter a valid number")
            self.wait_for_key()
            return self.get_clinic_selection(default_option)
    
    def get_doctor_selection(self, clinic_id: Optional[int] = None, default_option: bool = True) -> Optional[int]:
        """Display doctor selection interface
        
        Args:
            clinic_id (Optional[int]): Clinic ID, if specified only shows doctors from that clinic
            default_option (bool): Whether to show default option (all doctors)
            
        Returns:
            Optional[int]: Selected doctor ID, returns None if all doctors selected
                          Returns -1 to go back, if self.__should_return_to_main is True then return to main menu
        """
        self.print_header("Select Doctor")
        
        if clinic_id:
            doctors = self.__appointment_service.get_doctors_by_clinic(clinic_id)
            print(f"Doctors at clinic {clinic_id}:")
        else:
            doctors = self.__appointment_service.get_all_doctors()
            print("All doctors:")
        
        if not doctors:
            print("No doctor records found")
            self.wait_for_key()
            return -1
        
        print(f"{'ID':<5}{'Name':<15}{'Email':<25}{'Specialisation':<20}")
        print("-" * 65)
        
        for doctor in doctors:
            specialisation = ", ".join(doctor.specialisation)
            print(f"{doctor.id:<5}{doctor.full_name:<15}{doctor.email:<25}{specialisation:<20}")
        
        option_text = "\nSelect doctor ID"
        if default_option:
            option_text += ", or enter 0 to view all doctors/return"
        else:
            option_text += ", or enter 0 to return"
        option_text += ", enter - to return to main menu"
        option_text += ", press Enter to view all doctors by default: "
        
        print(option_text, end="")
        choice = input()
        
        if choice == "":
            return None  # Press Enter to view all doctors by default
        
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
                print("Invalid doctor ID")
                self.wait_for_key()
                return self.get_doctor_selection(clinic_id, default_option)
        except ValueError:
            print("Please enter a valid number")
            self.wait_for_key()
            return self.get_doctor_selection(clinic_id, default_option)
    
    def get_date_selection(self, future_only: bool = True, default_option: bool = True) -> Optional[str]:
        """Display date selection interface
        
        Args:
            future_only (bool): Whether to only show future dates
            default_option (bool): Whether to show default option (any date)
            
        Returns:
            Optional[str]: Selected date in YYYY-MM-DD format, returns None if any date selected
                          Returns empty string to go back, if self.__should_return_to_main is True then return to main menu
        """
        self.print_header("Select Date")
        
        today = self.__appointment_service.get_current_date()

        if future_only:
            dates = self.__appointment_service.get_date_range(today, 7)
            print("Future 7 days:")
        else:
            start_past = self.__DateUtil.shift_date(today, -7)
            past_dates = self.__appointment_service.get_date_range(start_past, 7)
            future_dates = self.__appointment_service.get_date_range(today, 7)
            dates = past_dates + future_dates
            print("Available dates (past 7 days and future 7 days):")
        
        print(f"{'Date':<15}{'Day of Week':<10}")
        print("-" * 25)
        
        for date in dates:
            day_of_week = self.__appointment_service.get_day_of_week(date)
            print(f"{date:<15}{day_of_week:<10}")
        
        option_text = "\nEnter date (YYYY-MM-DD)"
        if default_option:
            option_text += ", or enter 0 to view all dates/return"
        else:
            option_text += ", or enter 0 to return"
        option_text += ", enter - to return to main menu"
        option_text += f", press Enter to select today ({today}): "
        
        print(option_text, end="")
        choice = input()
        
        if choice == "":
            return today  # Press Enter to select today
        
        if choice == "-":
            self.__should_return_to_main = True
            return -1
        
        if choice == "0":
            return -1 if not default_option else None
        
        if not self.__appointment_service.is_valid_date(choice):
            print("Invalid date format, please use YYYY-MM-DD format")
            self.wait_for_key()
            return self.get_date_selection(future_only, default_option)
        
        if future_only and choice < today:
            print("Please select a future date")
            self.wait_for_key()
            return self.get_date_selection(future_only, default_option)
        
        return choice
    
    def show_available_slots(self, params: Dict[str, Any] = None) -> Optional[Tuple[str, int, int, int]]:
        """Display available time slot
        
        Args:
            params (Dict[str, Any], optional): Parameter dictionary, can include doctor_id, clinic_id, date
            
        Returns:
            Optional[Tuple[str, int, int, int]]: (date, time slot, doctor ID, clinic ID) tuple
                                                If user cancels then returns None
                                                If self.__should_return_to_main is True then return to main menu
        """
        params = params or {}
        
        # Get parameters
        clinic_id = params.get('clinic_id')
        doctor_id = params.get('doctor_id')
        date = params.get('date')
        
        # If clinic is not specified, let user choose
        if clinic_id is None:
            clinic_id = self.get_clinic_selection()
            if clinic_id == -1:  # User cancels or returns to main menu
                return None
        
        # If doctor is not specified, let user choose
        if doctor_id is None:
            doctor_id = self.get_doctor_selection(clinic_id)
            if doctor_id == -1:  # User cancels or returns to main menu
                return None
        
        # If date is not specified, let user choose
        if date is None:
            date = self.get_date_selection()
            if date == -1:  # User cancels or returns to main menu
                return None
        
        # If no filtering conditions are specified, user must select at least one
        if clinic_id is None and doctor_id is None and date is None:
            print("Please select at least one filtering condition (clinic, doctor, or date)")
            self.wait_for_key()
            return self.show_available_slots()
        
        self.print_header("Available Time Slots")
        
        # Get available time slots
        available_slots_data = self.__appointment_service.get_available_slots_data(clinic_id, doctor_id, date)
        
        if not available_slots_data:
            print("No available time slots found")
            self.wait_for_key()
            return None
        
        print("Available time slots:")
        print(f"{'Date':<15}{'Day of Week':<10}{'Clinic':<15}{'Doctor':<15}{'Available Time'}")
        print("-" * 85)
        
        option_index = 1
        for date_str, slot, d_id, c_id, clinic_name, doctor_name, day_of_week, time_str in available_slots_data:
            print(f"{option_index:2}. {date_str:<12} {day_of_week:<10} {clinic_name:<15} {doctor_name:<15} {time_str}")
            option_index += 1
        
        print("\nSelect time slot number, or enter 0 to return to previous menu, enter - to return to main menu, press Enter to select first: ", end="")
        choice = input()
        
        if choice == "":
            return available_slots_data[0][:4]  # Default select first available time slot (only return date, time slot, doctor ID, clinic ID)
        
        if choice == "-":
            self.__should_return_to_main = True
            return None
        
        if choice == "0":
            return None
        
        try:
            slot_index = int(choice) - 1
            if 0 <= slot_index < len(available_slots_data):
                return available_slots_data[slot_index][:4]  # Return selected time slot
            else:
                print("Invalid time slot number")
                self.wait_for_key()
                return None
        except ValueError:
            print("Please enter a valid number")
            self.wait_for_key()
            return None
    
    def make_appointment(self, user: User) -> None:
        """Appointment process
        
        Args:
            user (User): Current user
        """
        # Select available time slot
        slot_info = self.show_available_slots()
        if not slot_info:
            return
        
        date, time_slot, doctor_id, clinic_id = slot_info
        
        doctor = self.__appointment_service.get_doctor_by_id(doctor_id)
        clinic = self.__appointment_service.get_clinic_by_id(clinic_id)
        
        # Input appointment reason
        self.print_header("Appointment Information")
        print(f"Clinic: {clinic.name}")
        print(f"Doctor: {doctor.full_name}")
        print(f"Date: {date}")
        print(f"Time: {self.__appointment_service.get_time_slot_str(time_slot)}")
        
        reason = input("\nEnter appointment reason (Press Enter for default 'Regular Appointment'): ")
        if reason == "":
            reason = "Regular Appointment"  # Default appointment reason
        
        # Confirm appointment
        print("\nConfirm appointment information (Y/N), or enter 0 to return to previous menu, enter - to return to main menu, press Enter for default Y: ", end="")
        confirm = input().strip().upper()
        
        if confirm == "-":
            self.__should_return_to_main = True
            return
            
        if confirm == "0":
            return
            
        if confirm == "" or confirm == "Y":
            try:
                # Create appointment
                appointment = self.__appointment_service.make_appointment(
                    user.id, doctor_id, clinic_id, date, time_slot, reason
                )
                
                print("\nAppointment successful!")
                print(f"Appointment ID: {appointment.id}")
            except ValueError as e:
                print(f"\nAppointment failed: {str(e)}")
        else:
            print("Appointment cancelled")
            
        self.wait_for_key()
    
    def show_appointments(self, user: User, future_only: bool = False, history_only: bool = False) -> None:
        """Display appointment list
        
        Args:
            user (User): Current user
            future_only (bool): Whether to only show future appointments
            history_only (bool): Whether to only show history appointments
        """
        title = "My Appointments"
        if future_only:
            title = "Upcoming Appointments"
        elif history_only:
            title = "History Appointments"
            
        self.print_header(title)
        
        # Get appointment list
        appointments = self.__appointment_service.get_user_appointments(user.id, future_only, history_only)
        
        if not appointments:
            print("You have no appointment records" if not future_only and not history_only else "No appointments found that meet the criteria")
            self.wait_for_key()
            return
        
        print(f"{'ID':<5}{'Date':<15}{'Time':<20}{'Clinic':<15}{'Doctor':<15}{'Status':<15}")
        print("-" * 85)
        
        for appointment in appointments:
            print(f"{appointment['id']:<5}{appointment['date']:<15}{appointment['time_str']:<20}{appointment['clinic_name']:<15}{appointment['doctor_name']:<15}{appointment['status']:<15}")
        
        print("\nSelect appointment ID to view details, or enter 0 to return to previous menu, enter - to return to main menu, press Enter for default return: ", end="")
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
                print("Invalid appointment ID or you do not have permission to view this appointment")
                self.wait_for_key()
        except ValueError:
            print("Please enter a valid number")
            self.wait_for_key()
    
    def show_appointment_details(self, appointment_details: Dict) -> None:
        """Display appointment details
        
        Args:
            appointment_details (Dict): Appointment details dictionary
        """
        self.print_header("Appointment Details")
        
        print(f"Appointment ID: {appointment_details['id']}")
        print(f"User ID: {appointment_details['user_id']}")
        print(f"Patient Name: {appointment_details['user_name']}")
        print(f"Patient Email: {appointment_details['user_email']}")
        print(f"Date: {appointment_details['date']}")
        print(f"Time: {appointment_details['time_str']}")
        print(f"Clinic: {appointment_details['clinic_name']}")
        print(f"Clinic Address: {appointment_details['clinic_address']}")
        print(f"Doctor: {appointment_details['doctor_name']}")
        print(f"Appointment Reason: {appointment_details['reason']}")
        print(f"Status: {appointment_details['status']}")
        
        # Only cancellable appointments can be cancelled
        if appointment_details['can_cancel']:
            print("\n1. Cancel Appointment")
            print("0. Return to previous menu")
            print("-. Return to main menu")
            
            choice = input("\nSelect operation, press Enter for default return: ")
            
            if choice == "-":
                self.__should_return_to_main = True
                return
                
            if choice == "" or choice == "0":
                return
            
            if choice == "1":
                self.cancel_appointment(appointment_details['appointment_obj'])
        else:
            print("\n0. Return to previous menu")
            print("-. Return to main menu")
            choice = input("\nSelect operation, press Enter for default return: ")
            
            if choice == "-":
                self.__should_return_to_main = True
                return
                
            self.wait_for_key()
    
    def cancel_appointment(self, appointment) -> None:
        """Cancel appointment
        
        Args:
            appointment: Appointment object
        """
        print("\nConfirm cancellation (Y/N), or enter 0 to return to previous menu, enter - to return to main menu, press Enter for default N: ", end="")
        confirm = input().strip().upper()
        
        if confirm == "-":
            self.__should_return_to_main = True
            return
            
        if confirm == "0" or confirm == "":
            print("Operation cancelled")
            self.wait_for_key()
            return
        
        if confirm != "Y":
            print("Operation cancelled")
            self.wait_for_key()
            return
        
        # Cancel appointment
        if self.__appointment_service.cancel_appointment(appointment):
            print("\nAppointment cancelled successfully")
        else:
            print("\nAppointment cancellation failed, possibly appointment has already been cancelled")
        
        self.wait_for_key()

    def _show_all_appointments(self) -> None:
        """Display all system appointments (Admin only)"""
        self.print_header("All Appointments")
        appointments = self.__appointment_service.get_all_appointments()

        if not appointments:
            print("No appointments found")
            self.wait_for_key()
            return

        print(f"{'ID':<5}{'User ID':<8}{'Date':<12}{'Time':<18}{'Doctor':<15}{'Clinic':<15}{'Status':<12}")
        print("-" * 90)
        for appt in appointments:
            print(f"{appt['id']:<5}{appt['user_id']:<8}{appt['date']:<12}{appt['time_str']:<18}"
                  f"{appt['doctor_name']:<15}{appt['clinic_name']:<15}{appt['status']:<12}")
        
        print("\nSelect appointment ID to view details, or press 0 to return: ", end="")
        choice = input().strip()
        
        if choice == "0" or choice == "":
            return
            
        try:
            appt_id = int(choice)
            appt_details = self.__appointment_service.get_appointment_details(appt_id)
            if appt_details:
                self.show_appointment_details(appt_details)
                
                # Provide cancellation option
                if appt_details.get('status') == "Appointed":
                    if input("\nCancel this appointment? (Y/N): ").strip().upper() == "Y":
                        appointment = self.__appointment_service.get_appointment_by_id(appt_id)
                        if appointment:
                            if self.__appointment_service.cancel_appointment(appointment):
                                print("Appointment cancelled successfully")
                            else:
                                print("Appointment cancellation failed")
                        else:
                            print("Cannot retrieve appointment information")
            else:
                print("Invalid appointment ID")
        except ValueError:
            print("Please enter a valid number")
            
        self.wait_for_key()

    def _cancel_by_id(self) -> None:
        """Admin manually cancel any appointment"""
        self.print_header("Cancel Appointment by ID")
        
        try:
            appt_id = int(input("\nEnter appointment ID to cancel (0 to return): ").strip())
            if appt_id == 0:
                return
                
            appointment = self.__appointment_service.get_appointment_by_id(appt_id)
            if not appointment:
                print("Appointment does not exist")
                self.wait_for_key()
                return
                
            # Get detailed information and display
            appt_details = self.__appointment_service.get_appointment_details(appt_id)
            if appt_details:
                print("\nAppointment Details:")
                print(f"ID: {appt_details['id']}")
                print(f"User ID: {appt_details['user_id']}")
                print(f"Patient Name: {appt_details.get('user_name', 'Unknown')}")
                print(f"Date: {appt_details['date']}")
                print(f"Time: {appt_details['time_str']}")
                print(f"Clinic: {appt_details['clinic_name']}")
                print(f"Doctor: {appt_details['doctor_name']}")
                print(f"Current Status: {appt_details['status']}")
            
            if not appointment.is_scheduled():
                print("\nThis appointment status cannot be cancelled (possibly already cancelled or completed)")
                self.wait_for_key()
                return
                
            if input("\nConfirm cancellation of this appointment? (Y/N): ").strip().upper() == "Y":
                if self.__appointment_service.cancel_appointment(appointment):
                    print("Appointment cancelled successfully")
                else:
                    print("Cancellation failed")
            else:
                print("Operation cancelled")
        except ValueError:
            print("Please enter a valid number")
        self.wait_for_key()

    def _search_as_admin(self) -> None:
        """Admin filter appointments (no user_id restriction)"""
        dummy_user = User(id=-1)  # Used to bypass user_id restriction
        self.search_appointments(dummy_user)

    def search_appointments(self, user: User) -> None:
        """Search appointments
        
        Args:
            user (User): Current user
        """
        self.print_header("Search Appointments")
        
        print("Select filtering condition:")
        print("1. Filter by clinic")
        print("2. Filter by doctor")
        print("3. Filter by date")
        print("4. Filter by clinic and doctor")
        print("5. Filter by clinic and date")
        print("6. Filter by doctor and date")
        print("7. Filter by clinic, doctor, and date")
        print("0. Return to previous menu")
        print("-. Return to main menu")
        
        choice = input("\nSelect: ")
        
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
        """Display filtered appointment list
        
        Args:
            user (User): Current user
            params (Dict[str, Any]): Filter parameters
        """
        self.print_header("Filtered Results")
        
        # Get filtered appointments
        appointments = self.__appointment_service.filter_appointments(user.id, params)
        
        if not appointments:
            print("No appointments found that meet the criteria")
            self.wait_for_key()
            return
        
        print(f"{'ID':<5}{'User ID':<8}{'Date':<15}{'Time':<20}{'Clinic':<15}{'Doctor':<15}{'Status':<15}")
        print("-" * 95)
        
        for appointment in appointments:
            print(f"{appointment['id']:<5}{appointment['user_id']:<8}{appointment['date']:<15}{appointment['time_str']:<20}{appointment['clinic_name']:<15}{appointment['doctor_name']:<15}{appointment['status']:<15}")
        
        print("\nSelect appointment ID to view details, or enter 0 to return to previous menu, enter - to return to main menu, press Enter for default return: ", end="")
        choice = input()
        
        if choice == "-":
            self.__should_return_to_main = True
            return
            
        if choice == "" or choice == "0":
            return
        
        try:
            appointment_id = int(choice)
            appointment_details = self.__appointment_service.get_appointment_details(appointment_id)
            
            # Allow admin (user.id is -1) to view all appointment details
            if appointment_details and (appointment_details['user_id'] == user.id or user.id == -1):
                self.show_appointment_details(appointment_details)
            else:
                print("Invalid appointment ID or you do not have permission to view this appointment")
                self.wait_for_key()
        except ValueError:
            print("Please enter a valid number")
            self.wait_for_key()

    def run_appointment_menu(self, user: User) -> None:
        """Run appointment menu
        
        Args:
            user (User): Current user
        """
        self.__should_return_to_main = False  # Reset return to main menu flag
        
        while True:
            if self.__should_return_to_main:
                break
                
            self.print_header(f"Appointment Menu - {user.name}")
            
            print("1. Query available time slot and book")
            print("2. View all my appointments")
            print("3. View upcoming appointments")
            print("4. View history appointments")
            print("5. Search appointments")
            print("0. Return to previous menu")
            print("-. Return to main menu")
            
            choice = input("\nSelect operation: ")
            
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
                print("Invalid selection")
                self.wait_for_key()

    def run_admin_menu(self) -> None:
        """Admin appointment management menu"""
        self.__should_return_to_main = False  # Reset return to main menu flag
        
        while True:
            if self.__should_return_to_main:
                break
                
            self.print_header("Appointment Management - Admin")
            print("1. View all appointments")
            print("2. Filter appointments by condition")
            print("3. Cancel appointment by ID")
            print("0. Return to previous menu")
            print("-. Return to main menu")
            choice = input("\nSelect operation: ").strip()

            if choice == "1":
                self._show_all_appointments()
            elif choice == "2":
                self._search_as_admin()
            elif choice == "3":
                self._cancel_by_id()
            elif choice == "0":
                break
            elif choice == "-":
                self.__should_return_to_main = True
                break
            else:
                print("Invalid option")
                self.wait_for_key()
        
        return self.__should_return_to_main  # Return flag, for caller to determine whether to return to main menu

    def run(self):
        """Run appointment menu (compatible with UserController call method)"""
        if self.__current_user is None:
            print("Error: No user information provided")
            return
            
        self.run_appointment_menu(self.__current_user)
        
        # Return flag, for caller to determine whether to return to previous menu or main menu
        return self.__should_return_to_main
