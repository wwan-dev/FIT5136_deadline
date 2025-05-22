#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
user_controller.py
==================
• 登录入口
• 登录成功后展示用户菜单
• 当选择“预约管理”时，跳转至 AppointmentController
"""

from __future__ import annotations
import getpass
from typing import Optional

from src.services.user_service import UserService
from src.entities.user import User


class UserController:
    """处理用户相关的 CLI 交互"""

    def __init__(self):
        self._svc = UserService()
        self._current_user: Optional[User] = None

    # ───────────────────────── 登录流程 ─────────────────────────
    def run(self) -> None:
        """程序入口：循环直至成功登录或用户选择退出"""
        while True:
            print("\n===== MPMS Login =====")
            email = input("Email (enter 'q' to quit): ").strip()
            if email.lower() == "q":
                print("Goodbye.")
                return

            password = getpass.getpass("Password: ")
            success, user, msg = self._svc.login(email, password)
            print(msg)
            if success:
                self._current_user = user
                self._user_menu()
                # 退出登录后 _user_menu() 会 return，重回登录界面
            else:
                print("Please try again.\n")

    # ─────────────────────── 用户二级菜单 ───────────────────────
    def _user_menu(self) -> None:
        """登录成功后循环显示菜单，直到用户选择登出"""
        assert self._current_user is not None

        while True:
            print("\n===== User Menu =====")
            print("1. View Profile")
            print("2. Manage Appointments")
            print("0. Logout")

            choice = input("Select an option: ").strip()
            if choice == "1":
                self._show_profile()
            elif choice == "2":
                self._enter_appointment_menu()
            elif choice == "0":
                print("Logged out.\n")
                self._current_user = None
                return
            else:
                print("Invalid choice, please try again.")

    # ───────────────────────── 功能实现 ─────────────────────────
    def _show_profile(self) -> None:
        """打印用户资料（不含密码）"""
        profile = self._svc.get_profile(self._current_user)
        print("\n--- My Profile ---")
        for k, v in profile.items():
            if k != "password":
                print(f"{k.capitalize():15}: {v or '-'}")

    # 跳转到预约模块（此处仅做导入和调用，不实现逻辑）
    def _enter_appointment_menu(self) -> None:
        try:
            from src.controllers.appointment_controller import AppointmentController
            AppointmentController(self._current_user).run()
        except ModuleNotFoundError:
            print("Appointment module not available yet.")
        except Exception as e:
            print(f"Error when opening appointment menu: {e}")
