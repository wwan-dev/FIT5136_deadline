#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
User Controller
==============
• Login
• Route to Patient/Admin menu based on role
• This file only handles menu routing, specific business logic is delegated to AppointmentController/AdminController
"""

from __future__ import annotations
import getpass
from typing import Optional

from src.services.user_service import UserService
from src.entities.user import User


class UserController:
    """Top-level user interaction controller"""

    def __init__(self):
        self._svc = UserService()
        self._current_user: Optional[User] = None

    # ───────────────────────── Login Process ─────────────────────────
    def run(self) -> None:
        """Main application entry point"""
        while True:
            print("\n===== MPMS Login =====")
            email = input("Email (q to quit): ").strip()
            if email.lower() == "q":
                print("Bye.")
                return

            pwd = getpass.getpass("Password: ")
            ok, user, msg = self._svc.login(email, pwd)
            print(msg)
            if ok:
                self._current_user = user
                if user.is_admin():
                    self._admin_menu()
                else:
                    self._patient_menu()
                # Logout when menu returns
                self._current_user = None
            else:
                print()

    # --------------- Patient Menu ---------------
    def _patient_menu(self) -> None:
        """Display and handle patient menu options"""
        while True:
            # Check unread notification count
            unread_count = 0
            try:
                from src.controllers.notification_controller import NotificationController
                unread_count = NotificationController(self._current_user).check_unread_notifications()
            except Exception:
                pass
            
            print("\n===== Patient Menu =====")
            print("1. Manage Profile")
            print("2. Manage Appointments")
            print(f"3. Notifications {f'({unread_count} unread)' if unread_count > 0 else ''}")
            print("0. Logout")
            print("-. Main Menu")
            choice = input("Select: ").strip()

            if choice == "1":
                self._manage_profile()  # Sub-menu
            elif choice == "2":
                self._enter_appointment_menu()  # Sub-menu
            elif choice == "3":
                self._enter_notification_menu()  # Sub-menu
            elif choice == "0":  # Logout = return to login screen
                print("Logged out.")
                return
            elif choice == "-":  # Already in main menu; refresh screen
                continue
            else:
                print("Invalid choice.")

    # ─────────────────────── Admin Menu ───────────────────────
    def _admin_menu(self) -> None:
        """Display and handle admin menu options"""
        while True:
            print("\n===== Admin Menu =====")
            print(f"Current user: {self._current_user.name}, Role: {self._current_user.role}")
            print("1. Clinic / GP Management")
            print("2. Appointment Management")
            print("3. Reports / Statistics")
            print("0. Logout")
            print("-. Main Menu")

            choice = input("Select: ").strip()

            if choice == "1":
                self._enter_admin_controller("clinic")

            elif choice == "2":
                # Enter appointment management submenu (with global privileges)
                try:
                    from src.controllers.appointment_controller import AppointmentController
                    return_to_main = AppointmentController().run_admin_menu()
                    if return_to_main:
                        return  # Return directly to login screen
                except ModuleNotFoundError:
                    print("Appointment module not ready.")
                except Exception as e:
                    print(f"Error: {e}")

            elif choice == "3":
                self._enter_admin_controller("report")

            elif choice == "0":
                print("Logged out.")
                return  # Return to login screen

            elif choice == "-":
                continue  # Already in main menu; refresh

            else:
                print("Invalid choice.")

    # ───────────────────────── Common Functions ─────────────────────────
    # --------------- Profile Management ---------------
    def _manage_profile(self) -> None:
        """
        Display profile -> Select field -> Update -> Save
        """
        while True:
            profile = self._svc.get_profile(self._current_user)
            print("\n--- My Profile ---")
            for k, v in profile.items():
                if k != "password":
                    print(f"{k.capitalize():15}: {v or '-'}")

            print("\nEdit which field?")
            print(" 1. Name          2. Phone")
            print(" 3. Address       4. Date of Birth")
            print(" 5. Gender        6. Medical History")
            print(" 0. Back")
            sel = input("Select: ").strip()

            mapping = {
                "1": "name",
                "2": "phone",
                "3": "address",
                "4": "date_of_birth",
                "5": "gender",
                "6": "medical_history"
            }
            if sel == "0":
                return
            field = mapping.get(sel)
            if not field:
                print("Invalid option.")
                continue

            new_val = input(f"Enter new {field.replace('_', ' ')}: ")
            if self._svc.update_profile(self._current_user, field, new_val):
                print("Updated successfully.")
            else:
                print("Update failed (field not editable).")

    def _enter_appointment_menu(self) -> None:
        """Enter appointment management menu"""
        try:
            from src.controllers.appointment_controller import AppointmentController
            AppointmentController(self._current_user).run()
        except ModuleNotFoundError:
            print("Appointment module not ready.")
        except Exception as e:
            print(f"Error: {e}")
    
    def _enter_notification_menu(self) -> None:
        """Enter notification management menu"""
        try:
            from src.controllers.notification_controller import NotificationController
            return_to_main = NotificationController(self._current_user).run()
            if return_to_main:
                return  # Return to login screen
        except ModuleNotFoundError:
            print("Notification module not ready.")
            input("Press Enter to continue...")
        except Exception as e:
            print(f"Error: {e}")
            input("Press Enter to continue...")

    def _enter_admin_controller(self, mode: str) -> None:
        """
        Navigate to appropriate admin submodule based on mode
        
        Args:
            mode (str): The mode to enter, one of: "clinic", "appointment", "report"
        """
        if mode == "clinic":
            try:
                from src.controllers.clinic_controller import ClinicController
                return_to_main = ClinicController(self._current_user).run()
                if return_to_main:
                    return  # Return directly to login screen
            except ModuleNotFoundError:
                print("Clinic management module not ready.")
            except Exception as e:
                print(f"Error: {e}")
        elif mode == "report":
            try:
                from src.controllers.report_controller import ReportController
                return_to_main = ReportController(self._current_user).run()
                if return_to_main:
                    return  # Return directly to login screen
            except ModuleNotFoundError:
                print("Reports module not ready.")
            except Exception as e:
                print(f"Error: {e}")
            input("Press Enter to continue...")
        else:
            print(f"Unknown admin module: {mode}")
            input("Press Enter to continue...")
