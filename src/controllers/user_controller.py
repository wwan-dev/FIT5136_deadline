#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
user_controller.py
==================
• 登录
• 根据角色跳转到 Patient / Admin 主菜单
• 本文件只做菜单路由，具体业务分别交给 AppointmentController / AdminController
"""

from __future__ import annotations
import getpass
from typing import Optional

from src.services.user_service import UserService
from src.entities.user import User


class UserController:
    """顶层用户交互控制器"""

    def __init__(self):
        self._svc = UserService()
        self._current_user: Optional[User] = None

    # ───────────────────────── 登录流程 ─────────────────────────
    def run(self) -> None:
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
                # 菜单返回即登出
                self._current_user = None
            else:
                print()

    # --------------- 患者菜单 ---------------
    def _patient_menu(self) -> None:
        while True:
            print("\n===== Patient Menu =====")
            print("1. Manage Profile")         # ← 修改
            print("2. Manage Appointments")
            print("0. Logout")
            choice = input("Select: ").strip()

            if choice == "1":
                self._manage_profile()        # ← 新增
            elif choice == "2":
                self._enter_appointment_menu()
            elif choice == "0":
                print("Logged out.")
                return
            else:
                print("Invalid choice.")

    # ─────────────────────── 管理员菜单 ───────────────────────
    def _admin_menu(self) -> None:
        while True:
            print("\n===== Admin Menu =====")
            print("1. View Profile")
            print("2. Clinic / GP Management")
            print("3. Appointment Management")
            print("4. Reports / Statistics")
            print("0. Logout")
            choice = input("Select: ").strip()

            if choice == "1":
                self._show_profile()
            elif choice == "2":
                self._enter_admin_controller("clinic")
            elif choice == "3":
                self._enter_admin_controller("appointment")
            elif choice == "4":
                self._enter_admin_controller("report")
            elif choice == "0":
                print("Logged out.")
                return
            else:
                print("Invalid choice.")

    # ───────────────────────── 通用功能 ─────────────────────────
    # --------------- Profile 管理功能 ---------------
    def _manage_profile(self) -> None:
        """
        显示资料 → 选择字段 → 更新 → 保存
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
        try:
            from src.controllers.appointment_controller import AppointmentController
            AppointmentController(self._current_user).run()
        except ModuleNotFoundError:
            print("Appointment module not ready.")
        except Exception as e:
            print(f"Error: {e}")

    def _enter_admin_controller(self, mode: str) -> None:
        """
        根据 mode 跳转到相应管理员子模块
        mode ∈ {"clinic", "appointment", "report"}
        """
        # try:
        #     from src.controllers.admin_controller import AdminController
        #     AdminController(self._current_user, mode).run()
        # except ModuleNotFoundError:
        #     print("Admin module not ready.")
        # except Exception as e:
        #     print(f"Error: {e}")
        return None
