#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Clinic and Doctor Management Controller - Handles clinic and doctor management functions
"""

import os
from typing import Optional, Dict, Any, List

from src.entities.user import User
from src.entities.clinic import Clinic
from src.entities.doctor import Doctor
from src.repositories.clinic_repository import ClinicRepository
from src.repositories.doctor_repository import DoctorRepository

class ClinicController:
    """Clinic and Doctor Management Controller"""
    
    def __init__(self, user=None):
        """Initialize clinic and doctor management controller
        
        Args:
            user (User, optional): Current user. Defaults to None.
        """
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
        print()
    
    def wait_for_key(self):
        """Wait for user to press a key"""
        input("\nPress Enter to continue...")
    
    # ================ Clinic Management Functions ================
    def show_all_clinics(self) -> None:
        """Display all clinics"""
        self.print_header("All Clinics")
        
        clinics = self.__clinic_repo.get_all()
        
        if not clinics:
            print("No clinic records in the system")
            self.wait_for_key()
            return
        
        print(f"{'ID':<5}{'Name':<15}{'Suburb':<10}{'Address':<25}{'Phone':<15}")
        print("-" * 70)
        
        for clinic in clinics:
            print(f"{clinic.id:<5}{clinic.name:<15}{clinic.suburb:<10}{clinic.address:<25}{clinic.phone:<15}")
        
        print("\nSelect an option:")
        print("1. Add New Clinic")
        print("2. Edit Clinic")
        print("3. Delete Clinic")
        print("0. Return")
        print("-. Back to Main Menu")
        
        choice = input("\nSelect: ").strip()
        
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
            print("Invalid option")
            self.wait_for_key()
    
    def add_clinic(self) -> None:
        """Add a new clinic"""
        self.print_header("Add New Clinic")
        
        name = input("Clinic Name: ").strip()
        if not name:
            print("Name cannot be empty")
            self.wait_for_key()
            return
        
        # Check if clinic name already exists
        existing_clinic = self.__clinic_repo.get_by_name(name)
        if existing_clinic:
            print(f"Clinic '{name}' already exists")
            self.wait_for_key()
            return
        
        suburb = input("Suburb: ").strip()
        address = input("Address: ").strip()
        phone = input("Phone Number: ").strip()
        
        # Create new clinic
        new_clinic = Clinic(
            name=name,
            suburb=suburb,
            address=address,
            phone=phone
        )
        
        # Save clinic
        try:
            saved_clinic = self.__clinic_repo.add(new_clinic)
            print(f"\nSuccessfully added clinic: {saved_clinic.name} (ID: {saved_clinic.id})")
        except Exception as e:
            print(f"Failed to add clinic: {str(e)}")
        
        self.wait_for_key()
    
    def edit_clinic(self) -> None:
        """Edit clinic information"""
        self.print_header("Edit Clinic")
        
        clinic_id = input("Enter clinic ID to edit (0 to return): ").strip()
        
        if clinic_id == "0":
            return
        
        try:
            clinic_id = int(clinic_id)
            clinic = self.__clinic_repo.get_by_id(clinic_id)
            
            if not clinic:
                print(f"Cannot find clinic with ID {clinic_id}")
                self.wait_for_key()
                return
                
            print(f"\nCurrent clinic information:")
            print(f"ID: {clinic.id}")
            print(f"Name: {clinic.name}")
            print(f"Suburb: {clinic.suburb}")
            print(f"Address: {clinic.address}")
            print(f"Phone: {clinic.phone}")
            
            print("\nSelect field to edit:")
            print("1. Name")
            print("2. Suburb")
            print("3. Address")
            print("4. Phone")
            print("0. Return")
            
            field = input("\nSelect: ").strip()
            
            if field == "0":
                return
                
            if field == "1":
                new_name = input(f"New name (current: {clinic.name}): ").strip()
                if new_name:
                    clinic.name = new_name
            elif field == "2":
                new_suburb = input(f"New suburb (current: {clinic.suburb}): ").strip()
                if new_suburb:
                    clinic.suburb = new_suburb
            elif field == "3":
                new_address = input(f"New address (current: {clinic.address}): ").strip()
                if new_address:
                    clinic.address = new_address
            elif field == "4":
                new_phone = input(f"New phone (current: {clinic.phone}): ").strip()
                if new_phone:
                    clinic.phone = new_phone
            else:
                print("Invalid option")
                self.wait_for_key()
                return
            
            # Update clinic
            try:
                self.__clinic_repo.update(clinic)
                print("\nClinic information updated")
            except Exception as e:
                print(f"Failed to update clinic: {str(e)}")
            
        except ValueError:
            print("Invalid clinic ID")
        
        self.wait_for_key()
    
    def delete_clinic(self) -> None:
        """Delete a clinic"""
        self.print_header("Delete Clinic")
        
        clinic_id = input("Enter clinic ID to delete (0 to return): ").strip()
        
        if clinic_id == "0":
            return
        
        try:
            clinic_id = int(clinic_id)
            clinic = self.__clinic_repo.get_by_id(clinic_id)
            
            if not clinic:
                print(f"Cannot find clinic with ID {clinic_id}")
                self.wait_for_key()
                return
                
            # Check if there are doctors associated with this clinic
            doctors = self.__doctor_repo.get_by_clinic(clinic_id)
            if doctors:
                print(f"Cannot delete clinic, there are {len(doctors)} doctors associated with it")
                print("Please remove these doctors from the clinic first")
                self.wait_for_key()
                return
            
            print(f"\nAbout to delete clinic: {clinic.name} (ID: {clinic.id})")
            confirm = input("Confirm deletion? (Y/N): ").strip().upper()
            
            if confirm == "Y":
                try:
                    self.__clinic_repo.delete(clinic.id)
                    print("\nClinic deleted")
                except Exception as e:
                    print(f"Failed to delete clinic: {str(e)}")
            else:
                print("Deletion cancelled")
            
        except ValueError:
            print("Invalid clinic ID")
        
        self.wait_for_key()
    
    def search_clinics(self) -> None:
        """Search for clinics"""
        self.print_header("Search Clinics")
        
        keyword = input("Enter search keyword (0 to return): ").strip()
        
        if keyword == "0":
            return
        
        if not keyword:
            print("Search keyword cannot be empty")
            self.wait_for_key()
            return
        
        clinics = self.__clinic_repo.search(keyword)
        
        if not clinics:
            print(f"No clinics found matching '{keyword}'")
            self.wait_for_key()
            return
        
        print(f"\nFound {len(clinics)} matching clinics:")
        print(f"{'ID':<5}{'Name':<15}{'Suburb':<10}{'Address':<25}{'Phone':<15}")
        print("-" * 70)
        
        for clinic in clinics:
            print(f"{clinic.id:<5}{clinic.name:<15}{clinic.suburb:<10}{clinic.address:<25}{clinic.phone:<15}")
        
        self.wait_for_key()
    
    # ================ Doctor Management Functions ================
    def show_all_doctors(self) -> None:
        """Display all doctors"""
        self.print_header("All Doctors")
        
        doctors = self.__doctor_repo.get_all()
        
        if not doctors:
            print("No doctor records in the system")
            self.wait_for_key()
            return
        
        print(f"{'ID':<5}{'Name':<15}{'Email':<25}{'Specialisation':<25}")
        print("-" * 70)
        
        for doctor in doctors:
            specialisations = ", ".join(doctor.specialisation)
            print(f"{doctor.id:<5}{doctor.full_name:<15}{doctor.email:<25}{specialisations:<25}")
        
        print("\nSelect an option:")
        print("1. Add New Doctor")
        print("2. Edit Doctor")
        print("3. Delete Doctor")
        print("4. Manage Doctor Clinic Association")
        print("0. Return")
        print("-. Back to Main Menu")
        
        choice = input("\nSelect: ").strip()
        
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
            print("Invalid option")
            self.wait_for_key()
    
    def add_doctor(self) -> None:
        """Add a new doctor"""
        self.print_header("Add New Doctor")
        
        full_name = input("Doctor Name: ").strip()
        if not full_name:
            print("Name cannot be empty")
            self.wait_for_key()
            return
        
        email = input("Email: ").strip()
        if not email:
            print("Email cannot be empty")
            self.wait_for_key()
            return
        
        # Check if email already exists
        existing_doctor = self.__doctor_repo.get_by_email(email)
        if existing_doctor:
            print(f"Email '{email}' already exists")
            self.wait_for_key()
            return
        
        # Specialisation - Changed to input in one line, separated by semicolon
        spec_input = input("Specialisation (use semicolon ';' to separate multiple specialisations): ").strip()
        specialisations = [spec.strip() for spec in spec_input.split(';') if spec.strip()]
        
        # Create new doctor
        new_doctor = Doctor(
            full_name=full_name,
            email=email,
            specialisation=specialisations
        )
        
        # Save doctor
        try:
            saved_doctor = self.__doctor_repo.add(new_doctor)
            print(f"\nSuccessfully added doctor: {saved_doctor.full_name} (ID: {saved_doctor.id})")
        except Exception as e:
            print(f"Failed to add doctor: {str(e)}")
        
        self.wait_for_key()
    
    def edit_doctor(self) -> None:
        """Edit doctor information"""
        self.print_header("Edit Doctor")
        
        doctor_id = input("Enter doctor ID to edit (0 to return): ").strip()
        
        if doctor_id == "0":
            return
        
        try:
            doctor_id = int(doctor_id)
            doctor = self.__doctor_repo.get_by_id(doctor_id)
            
            if not doctor:
                print(f"Cannot find doctor with ID {doctor_id}")
                self.wait_for_key()
                return
                
            print(f"\nCurrent doctor information:")
            print(f"ID: {doctor.id}")
            print(f"Name: {doctor.full_name}")
            print(f"Email: {doctor.email}")
            print(f"Specialisation: {', '.join(doctor.specialisation)}")
            
            print("\nSelect field to edit:")
            print("1. Name")
            print("2. Email")
            print("3. Manage Specialisation")
            print("0. Return")
            
            field = input("\nSelect: ").strip()
            
            if field == "0":
                return
                
            if field == "1":
                new_name = input(f"New name (current: {doctor.full_name}): ").strip()
                if new_name:
                    doctor.full_name = new_name
            elif field == "2":
                new_email = input(f"New email (current: {doctor.email}): ").strip()
                if new_email:
                    doctor.email = new_email
            elif field == "3":
                self.manage_doctor_specialisations(doctor)
                return
            else:
                print("Invalid option")
                self.wait_for_key()
                return
            
            # Update doctor
            try:
                self.__doctor_repo.update(doctor)
                print("\nDoctor information updated")
            except Exception as e:
                print(f"Failed to update doctor: {str(e)}")
            
        except ValueError:
            print("Invalid doctor ID")
        
        self.wait_for_key()
    
    def manage_doctor_specialisations(self, doctor: Doctor) -> None:
        """Manage doctor specialisation
        
        Args:
            doctor (Doctor): The doctor whose specialisations are being managed
        """
        while True:
            self.print_header(f"Manage Doctor {doctor.full_name} Specialisation")
            
            print("Current specialisation:")
            if doctor.specialisation:
                for i, spec in enumerate(doctor.specialisation, 1):
                    print(f"{i}. {spec}")
            else:
                print("(None)")
            
            print("\nSelect an option:")
            print("1. Add Specialisation")
            print("2. Delete Specialisation")
            print("0. Return")
            
            choice = input("\nSelect: ").strip()
            
            if choice == "0":
                return
                
            if choice == "1":
                # Add specialisation, support adding multiple at once, separated by semicolon
                spec_input = input("Specialisation (use semicolon ';' to separate multiple specialisations): ").strip()
                new_specs = [spec.strip() for spec in spec_input.split(';') if spec.strip()]
                
                # Add each specialisation
                added_count = 0
                for new_spec in new_specs:
                    doctor.add_specialisation(new_spec)
                    added_count += 1
                
                if added_count > 0:
                    try:
                        self.__doctor_repo.update(doctor)
                        print(f"Added {added_count} specialisations")
                    except Exception as e:
                        print(f"Failed to update: {str(e)}")
                else:
                    print("No specialisations added")
                self.wait_for_key()
            elif choice == "2":
                if not doctor.specialisation:
                    print("No specialisations to delete")
                    self.wait_for_key()
                    continue
                
                # Display specialisation list with index
                print("\nCurrent specialisation:")
                for i, spec in enumerate(doctor.specialisation, 1):
                    print(f"{i}. {spec}")
                
                try:
                    # Support deleting multiple specialisations, separated by comma
                    index_input = input("\nEnter specialisation index to delete (multiple with comma): ").strip()
                    indexes = [int(idx.strip()) for idx in index_input.split(',') if idx.strip().isdigit()]
                    
                    # Sort and reverse, delete from back to front to avoid index change issues
                    indexes.sort(reverse=True)
                    removed_specs = []
                    
                    for idx in indexes:
                        if 1 <= idx <= len(doctor.specialisation):
                            spec_to_remove = doctor.specialisation[idx-1]
                            doctor.remove_specialisation(spec_to_remove)
                            removed_specs.append(spec_to_remove)
                    
                    if removed_specs:
                        try:
                            self.__doctor_repo.update(doctor)
                            print(f"Deleted specialisation: {', '.join(removed_specs)}")
                        except Exception as e:
                            print(f"Failed to update: {str(e)}")
                    else:
                        print("No specialisations deleted")
                except ValueError:
                    print("Enter valid number")
                self.wait_for_key()
            else:
                print("Invalid option")
                self.wait_for_key()
    
    def delete_doctor(self) -> None:
        """Delete a doctor"""
        self.print_header("Delete Doctor")
        
        doctor_id = input("Enter doctor ID to delete (0 to return): ").strip()
        
        if doctor_id == "0":
            return
        
        try:
            doctor_id = int(doctor_id)
            doctor = self.__doctor_repo.get_by_id(doctor_id)
            
            if not doctor:
                print(f"Cannot find doctor with ID {doctor_id}")
                self.wait_for_key()
                return
            
            print(f"\nAbout to delete doctor: {doctor.full_name} (ID: {doctor.id})")
            confirm = input("Confirm deletion? (Y/N): ").strip().upper()
            
            if confirm == "Y":
                try:
                    self.__doctor_repo.delete(doctor.id)
                    print("\nDoctor deleted")
                except Exception as e:
                    print(f"Failed to delete doctor: {str(e)}")
            else:
                print("Deletion cancelled")
            
        except ValueError:
            print("Invalid doctor ID")
        
        self.wait_for_key()
    
    def manage_doctor_clinics(self) -> None:
        """Manage doctor clinic association"""
        self.print_header("Manage Doctor Clinic Association")
        
        doctor_id = input("Enter doctor ID (0 to return): ").strip()
        
        if doctor_id == "0":
            return
        
        try:
            doctor_id = int(doctor_id)
            doctor = self.__doctor_repo.get_by_id(doctor_id)
            
            if not doctor:
                print(f"Cannot find doctor with ID {doctor_id}")
                self.wait_for_key()
                return
            
            while True:
                self.print_header(f"Manage Doctor {doctor.full_name} Clinic Association")
                
                # Display current associated clinics
                print("Current associated clinics:")
                if doctor.assigned_clinics:
                    for clinic_id in doctor.assigned_clinics:
                        clinic = self.__clinic_repo.get_by_id(clinic_id)
                        if clinic:
                            print(f"ID: {clinic.id}, Name: {clinic.name}, Suburb: {clinic.suburb}")
                else:
                    print("(None)")
                
                print("\nSelect an option:")
                print("1. Add Clinic Association")
                print("2. Remove Clinic Association")
                print("0. Return")
                
                choice = input("\nSelect: ").strip()
                
                if choice == "0":
                    return
                    
                if choice == "1":
                    self.add_clinic_to_doctor(doctor)
                elif choice == "2":
                    self.remove_clinic_from_doctor(doctor)
                else:
                    print("Invalid option")
                    self.wait_for_key()
            
        except ValueError:
            print("Invalid doctor ID")
            self.wait_for_key()
    
    def add_clinic_to_doctor(self, doctor: Doctor) -> None:
        """Add clinic association to doctor
        
        Args:
            doctor (Doctor): The doctor to add clinic association to
        """
        self.print_header(f"Add Clinic to Doctor {doctor.full_name}")
        
        # Display all clinics
        clinics = self.__clinic_repo.get_all()
        
        if not clinics:
            print("No clinic records in the system")
            self.wait_for_key()
            return
        
        print("Available clinics:")
        available_clinics = []
        for clinic in clinics:
            if clinic.id not in doctor.assigned_clinics:
                available_clinics.append(clinic)
                print(f"ID: {clinic.id}, Name: {clinic.name}, Suburb: {clinic.suburb}")
        
        if not available_clinics:
            print("No clinics to add")
            self.wait_for_key()
            return
        
        try:
            clinic_id = int(input("\nEnter clinic ID to add (0 to return): ").strip())
            
            if clinic_id == 0:
                return
            
            # Check if clinic ID is valid
            clinic = self.__clinic_repo.get_by_id(clinic_id)
            if not clinic:
                print(f"Cannot find clinic with ID {clinic_id}")
                self.wait_for_key()
                return
            
            # Check if already associated
            if clinic.id in doctor.assigned_clinics:
                print(f"Doctor already associated with clinic {clinic.name}")
                self.wait_for_key()
                return
            
            # Add association
            doctor.add_clinic(clinic.id)
            
            # Update doctor
            try:
                self.__doctor_repo.update(doctor)
                print(f"\nAdded doctor {doctor.full_name} to clinic {clinic.name}")
            except Exception as e:
                print(f"Failed to update: {str(e)}")
            
        except ValueError:
            print("Invalid clinic ID")
        
        self.wait_for_key()
    
    def remove_clinic_from_doctor(self, doctor: Doctor) -> None:
        """Remove clinic association from doctor
        
        Args:
            doctor (Doctor): The doctor to remove clinic association from
        """
        self.print_header(f"Remove Clinic from Doctor {doctor.full_name}")
        
        if not doctor.assigned_clinics:
            print("Doctor has no associated clinics")
            self.wait_for_key()
            return
        
        print("Current associated clinics:")
        for clinic_id in doctor.assigned_clinics:
            clinic = self.__clinic_repo.get_by_id(clinic_id)
            if clinic:
                print(f"ID: {clinic.id}, Name: {clinic.name}, Suburb: {clinic.suburb}")
        
        try:
            clinic_id = int(input("\nEnter clinic ID to remove (0 to return): ").strip())
            
            if clinic_id == 0:
                return
            
            # Check if clinic ID is associated
            if clinic_id not in doctor.assigned_clinics:
                print(f"Doctor not associated with ID {clinic_id} clinic")
                self.wait_for_key()
                return
            
            # Get clinic name
            clinic = self.__clinic_repo.get_by_id(clinic_id)
            clinic_name = clinic.name if clinic else f"ID {clinic_id}"
            
            # Remove association
            doctor.remove_clinic(clinic_id)
            
            # Update doctor
            try:
                self.__doctor_repo.update(doctor)
                print(f"\nRemoved doctor {doctor.full_name} from clinic {clinic_name}")
            except Exception as e:
                print(f"Failed to update: {str(e)}")
            
        except ValueError:
            print("Invalid clinic ID")
        
        self.wait_for_key()
    
    def search_doctors(self) -> None:
        """Search for doctors"""
        self.print_header("Search Doctors")
        
        keyword = input("Enter search keyword (0 to return): ").strip()
        
        if keyword == "0":
            return
        
        if not keyword:
            print("Search keyword cannot be empty")
            self.wait_for_key()
            return
        
        doctors = self.__doctor_repo.search(keyword)
        
        if not doctors:
            print(f"No doctors found matching '{keyword}'")
            self.wait_for_key()
            return
        
        print(f"\nFound {len(doctors)} matching doctors:")
        print(f"{'ID':<5}{'Name':<15}{'Email':<25}{'Specialisation':<25}")
        print("-" * 70)
        
        for doctor in doctors:
            specialisations = ", ".join(doctor.specialisation)
            print(f"{doctor.id:<5}{doctor.full_name:<15}{doctor.email:<25}{specialisations:<25}")
        
        self.wait_for_key()
    
    # ================ Main Menu ================
    def run(self) -> None:
        """Run clinic and doctor management menu
        
        Returns:
            bool: Flag indicating whether to return to main menu
        """
        self.__should_return_to_main = False  # Reset return to main menu flag
        
        while True:
            if self.__should_return_to_main:
                break
                
            self.print_header("Clinic and Doctor Management")
            
            print("1. View All Clinics")
            print("2. Search Clinics")
            print("3. View All Doctors")
            print("4. Search Doctors")
            print("0. Return")
            print("-. Back to Main Menu")
            
            choice = input("\nSelect operation: ").strip()
            
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
                print("Invalid option")
                self.wait_for_key()
        
        return self.__should_return_to_main  # Return flag, for caller to determine if returning to main menu 