#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通知控制器类 - 处理通知UI界面和交互
"""

import os
from typing import Optional, List
from datetime import datetime

from src.entities.user import User
from src.entities.notification import Notification
from src.services.notification_service import NotificationService

class NotificationController:
    """通知控制器类"""
    
    def __init__(self, user=None):
        """初始化通知控制器
        
        Args:
            user (User, optional): 当前用户. Defaults to None.
        """
        self.__notification_svc = NotificationService()
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
    
    def show_notifications(self) -> None:
        """显示用户通知列表"""
        if not self.__current_user:
            print("用户未登录")
            self.wait_for_key()
            return
        
        while True:
            self.print_header("我的通知")
            
            # 获取用户通知
            notifications = self.__notification_svc.get_notifications_by_user(self.__current_user.id)
            
            if not notifications:
                print("您没有任何通知")
                self.wait_for_key()
                return
            
            # 显示通知列表
            print(f"{'ID':<5}{'日期':<12}{'状态':<8}{'内容':<50}")
            print("-" * 75)
            
            for notification in notifications:
                # 状态显示为"已读"或"未读"
                status = "已读" if notification.read else "未读"
                # 截取过长的消息
                message = notification.message[:47] + "..." if len(notification.message) > 50 else notification.message
                print(f"{notification.id:<5}{notification.date:<12}{status:<8}{message:<50}")
            
            print("\n请选择操作:")
            print("1. 查看通知详情")
            print("2. 标记通知为已读")
            print("3. 标记所有通知为已读")
            print("0. 返回")
            print("-. 返回主菜单")
            
            choice = input("\n请选择: ").strip()
            
            if choice == "-":
                self.__should_return_to_main = True
                return
                
            if choice == "0":
                return
                
            if choice == "1":
                self.view_notification_detail()
            elif choice == "2":
                self.mark_notification_as_read()
            elif choice == "3":
                self.mark_all_as_read()
            else:
                print("无效选项")
                self.wait_for_key()
    
    def view_notification_detail(self) -> None:
        """查看通知详情"""
        self.print_header("通知详情")
        
        notification_id = input("请输入要查看的通知ID (0返回): ").strip()
        
        if notification_id == "0":
            return
        
        try:
            notification_id = int(notification_id)
            notification = self.__notification_svc.get_notification_by_id(notification_id)
            
            if not notification:
                print(f"找不到ID为 {notification_id} 的通知")
                self.wait_for_key()
                return
            
            # 检查该通知是否属于当前用户
            if notification.user_id != self.__current_user.id:
                print("您无权查看此通知")
                self.wait_for_key()
                return
            
            # 显示通知详情
            print(f"ID: {notification.id}")
            print(f"日期: {notification.date}")
            print(f"状态: {'已读' if notification.read else '未读'}")
            print(f"内容: {notification.message}")
            
            # 如果通知未读，标记为已读
            if not notification.read:
                mark_read = input("\n是否标记为已读? (Y/N): ").strip().upper()
                if mark_read == "Y":
                    if self.__notification_svc.mark_notification_as_read(notification.id):
                        print("已标记为已读")
                    else:
                        print("标记失败")
                
        except ValueError:
            print("无效的通知ID")
        
        self.wait_for_key()
    
    def mark_notification_as_read(self) -> None:
        """标记单个通知为已读"""
        self.print_header("标记通知为已读")
        
        notification_id = input("请输入要标记为已读的通知ID (0返回): ").strip()
        
        if notification_id == "0":
            return
        
        try:
            notification_id = int(notification_id)
            notification = self.__notification_svc.get_notification_by_id(notification_id)
            
            if not notification:
                print(f"找不到ID为 {notification_id} 的通知")
                self.wait_for_key()
                return
            
            # 检查该通知是否属于当前用户
            if notification.user_id != self.__current_user.id:
                print("您无权操作此通知")
                self.wait_for_key()
                return
            
            # 检查通知是否已读
            if notification.read:
                print("此通知已经标记为已读")
                self.wait_for_key()
                return
            
            # 标记为已读
            if self.__notification_svc.mark_notification_as_read(notification.id):
                print("已标记为已读")
            else:
                print("标记失败")
            
        except ValueError:
            print("无效的通知ID")
        
        self.wait_for_key()
    
    def mark_all_as_read(self) -> None:
        """标记所有通知为已读"""
        self.print_header("标记所有通知为已读")
        
        confirm = input("确认要将所有通知标记为已读? (Y/N): ").strip().upper()
        
        if confirm != "Y":
            print("已取消操作")
            self.wait_for_key()
            return
        
        # 标记所有通知为已读
        count = self.__notification_svc.mark_all_notifications_as_read(self.__current_user.id)
        
        if count > 0:
            print(f"已将 {count} 条通知标记为已读")
        else:
            print("没有未读通知")
        
        self.wait_for_key()
    
    def check_unread_notifications(self) -> int:
        """检查未读通知数量
        
        Returns:
            int: 未读通知数量
        """
        if not self.__current_user:
            return 0
        
        unread = self.__notification_svc.get_unread_notifications(self.__current_user.id)
        return len(unread)
    
    def run(self) -> bool:
        """运行通知菜单
        
        Returns:
            bool: 是否返回主菜单
        """
        self.__should_return_to_main = False  # 重置返回主菜单标志
        self.show_notifications()
        return self.__should_return_to_main  # 返回标志，供调用者判断是否返回主菜单 