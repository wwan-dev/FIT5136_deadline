#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Notification Controller - Handles notification UI and interactions
"""

import os
from typing import Optional, List
from datetime import datetime

from src.entities.user import User
from src.entities.notification import Notification
from src.services.notification_service import NotificationService

class NotificationController:
    """Notification Controller"""
    
    def __init__(self, user=None):
        """Initialize notification controller
        
        Args:
            user (User, optional): Current user. Defaults to None.
        """
        self.__notification_svc = NotificationService()
        self.__current_user = user
        self.__should_return_to_main = False  # Flag to return to main menu
    
    def clear_screen(self):
        """Clear screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print title header"""
        self.clear_screen()
        print("=" * 50)
        print(f"{title.center(48)}")
        print("=" * 50)
        print()
    
    def wait_for_key(self):
        """Wait for user to press a key"""
        input("\nPress Enter to continue...")
    
    def show_notifications(self) -> None:
        """Display user notifications list"""
        if not self.__current_user:
            print("User not logged in")
            self.wait_for_key()
            return
        
        while True:
            self.print_header("My Notifications")
            
            # Get user notifications
            notifications = self.__notification_svc.get_notifications_by_user(self.__current_user.id)
            
            if not notifications:
                print("You don't have any notifications")
                self.wait_for_key()
                return
            
            # Display notification list
            print(f"{'ID':<5}{'Date':<12}{'Status':<8}{'Content':<50}")
            print("-" * 75)
            
            for notification in notifications:
                # Status displayed as "Read" or "Unread"
                status = "Read" if notification.read else "Unread"
                # Truncate long messages
                message = notification.message[:47] + "..." if len(notification.message) > 50 else notification.message
                print(f"{notification.id:<5}{notification.date:<12}{status:<8}{message:<50}")
            
            print("\nSelect an option:")
            print("1. View Notification Details")
            print("2. Mark Notification as Read")
            print("3. Mark All Notifications as Read")
            print("0. Return")
            print("-. Back to Main Menu")
            
            choice = input("\nSelect: ").strip()
            
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
                print("Invalid option")
                self.wait_for_key()
    
    def view_notification_detail(self) -> None:
        """View notification details"""
        self.print_header("Notification Details")
        
        notification_id = input("Enter notification ID to view (0 to return): ").strip()
        
        if notification_id == "0":
            return
        
        try:
            notification_id = int(notification_id)
            notification = self.__notification_svc.get_notification_by_id(notification_id)
            
            if not notification:
                print(f"Cannot find notification with ID {notification_id}")
                self.wait_for_key()
                return
            
            # Check if the notification belongs to current user
            if notification.user_id != self.__current_user.id:
                print("You don't have permission to view this notification")
                self.wait_for_key()
                return
            
            # Display notification details
            print(f"ID: {notification.id}")
            print(f"Date: {notification.date}")
            print(f"Status: {'Read' if notification.read else 'Unread'}")
            print(f"Content: {notification.message}")
            
            # If notification is unread, offer to mark as read
            if not notification.read:
                mark_read = input("\nMark as read? (Y/N): ").strip().upper()
                if mark_read == "Y":
                    if self.__notification_svc.mark_notification_as_read(notification.id):
                        print("Marked as read")
                    else:
                        print("Failed to mark as read")
                
        except ValueError:
            print("Invalid notification ID")
        
        self.wait_for_key()
    
    def mark_notification_as_read(self) -> None:
        """Mark a single notification as read"""
        self.print_header("Mark Notification as Read")
        
        notification_id = input("Enter notification ID to mark as read (0 to return): ").strip()
        
        if notification_id == "0":
            return
        
        try:
            notification_id = int(notification_id)
            notification = self.__notification_svc.get_notification_by_id(notification_id)
            
            if not notification:
                print(f"Cannot find notification with ID {notification_id}")
                self.wait_for_key()
                return
            
            # Check if the notification belongs to current user
            if notification.user_id != self.__current_user.id:
                print("You don't have permission to modify this notification")
                self.wait_for_key()
                return
            
            # Check if notification is already read
            if notification.read:
                print("This notification is already marked as read")
                self.wait_for_key()
                return
            
            # Mark as read
            if self.__notification_svc.mark_notification_as_read(notification.id):
                print("Marked as read")
            else:
                print("Failed to mark as read")
            
        except ValueError:
            print("Invalid notification ID")
        
        self.wait_for_key()
    
    def mark_all_as_read(self) -> None:
        """Mark all notifications as read"""
        self.print_header("Mark All Notifications as Read")
        
        confirm = input("Confirm marking all notifications as read? (Y/N): ").strip().upper()
        
        if confirm != "Y":
            print("Operation cancelled")
            self.wait_for_key()
            return
        
        # Mark all notifications as read
        count = self.__notification_svc.mark_all_notifications_as_read(self.__current_user.id)
        
        if count > 0:
            print(f"Marked {count} notifications as read")
        else:
            print("No unread notifications")
        
        self.wait_for_key()
    
    def check_unread_notifications(self) -> int:
        """Check number of unread notifications
        
        Returns:
            int: Number of unread notifications
        """
        if not self.__current_user:
            return 0
        
        unread = self.__notification_svc.get_unread_notifications(self.__current_user.id)
        return len(unread)
    
    def run(self) -> bool:
        """Run notification menu
        
        Returns:
            bool: Whether to return to main menu
        """
        self.__should_return_to_main = False  # Reset return to main menu flag
        self.show_notifications()
        return self.__should_return_to_main  # Return flag, for caller to determine if returning to main menu 