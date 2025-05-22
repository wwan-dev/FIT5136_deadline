#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date utility class, provides date and time slot related operations
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class DateUtil:
    """Date utility class, provides date and time slot related operations"""
    
    # Time slot mapping, each time slot corresponds to half an hour
    TIME_SLOT_MAP = {
        1: "9:00 AM - 9:30 AM",
        2: "9:30 AM - 10:00 AM",
        3: "10:00 AM - 10:30 AM",
        4: "10:30 AM - 11:00 AM",
        5: "11:00 AM - 11:30 AM",
        6: "11:30 AM - 12:00 PM",
        7: "12:00 PM - 12:30 PM",
        8: "12:30 PM - 1:00 PM",
        9: "1:00 PM - 1:30 PM",
        10: "1:30 PM - 2:00 PM",
        11: "2:00 PM - 2:30 PM",
        12: "2:30 PM - 3:00 PM",
        13: "3:00 PM - 3:30 PM",
        14: "3:30 PM - 4:00 PM",
        15: "4:00 PM - 4:30 PM",
        16: "4:30 PM - 5:00 PM"
    }
    
    @staticmethod
    def get_time_slot_str(time_slot: int) -> str:
        """Get string representation of time slot
        
        Args:
            time_slot (int): Time slot index (1-16)
            
        Returns:
            str: String representation of time slot
        """
        if time_slot in DateUtil.TIME_SLOT_MAP:
            return DateUtil.TIME_SLOT_MAP[time_slot]
        return "Unknown Time Slot"
    
    @staticmethod
    def get_time_slot_from_str(time_str: str) -> int:
        """Get time slot index from string
        
        Args:
            time_str (str): Time string
            
        Returns:
            int: Time slot index (1-16), returns 0 if no match
        """
        for slot, slot_str in DateUtil.TIME_SLOT_MAP.items():
            if slot_str == time_str:
                return slot
        return 0
    
    @staticmethod
    def get_current_date() -> str:
        """Get current date
        
        Returns:
            str: Current date in format "YYYY-MM-DD"
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_date_range(start_date: str, days: int) -> List[str]:
        """Get date range
        
        Args:
            start_date (str): Start date in format "YYYY-MM-DD"
            days (int): Number of days
            
        Returns:
            List[str]: List of dates
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        date_list = []
        
        for i in range(days):
            date = start + timedelta(days=i)
            date_list.append(date.strftime("%Y-%m-%d"))
        
        return date_list
    
    @staticmethod
    def is_future_date(date_str: str) -> bool:
        """Check if date is in the future
        
        Args:
            date_str (str): Date in format "YYYY-MM-DD"
            
        Returns:
            bool: True if date is in the future, False otherwise
        """
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            today = datetime.now().date()
            return date > today
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        """Check if date is valid
        
        Args:
            date_str (str): Date in format "YYYY-MM-DD"
            
        Returns:
            bool: True if date is valid, False otherwise
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def format_date(date_str: str, input_format: str = "%Y-%m-%d", output_format: str = "%d/%m/%Y") -> str:
        """Format date
        
        Args:
            date_str (str): Date string
            input_format (str, optional): Input format. Defaults to "%Y-%m-%d".
            output_format (str, optional): Output format. Defaults to "%d/%m/%Y".
            
        Returns:
            str: Formatted date string
        """
        try:
            date = datetime.strptime(date_str, input_format)
            return date.strftime(output_format)
        except ValueError:
            return date_str
    
    @staticmethod
    def get_day_of_week(date_str: str) -> str:
        """Get day of week
        
        Args:
            date_str (str): Date in format "YYYY-MM-DD"
            
        Returns:
            str: Day of week
        """
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            return days[date.weekday()]
        except ValueError:
            return "Unknown"
    
    @staticmethod
    def time_slots_to_hex(time_slots: List[int]) -> str:
        """Convert time slot list to hexadecimal string
        
        Args:
            time_slots (List[int]): List of time slot indices (1-16)
            
        Returns:
            str: Hexadecimal string
        """
        if not time_slots:
            return "0"
        
        value = 0
        for slot in time_slots:
            if 1 <= slot <= 16:
                # Since time slots are 1-16 and bits are 0-15, need to subtract 1
                value |= (1 << (slot - 1))
        
        return format(value, 'x')
    
    @staticmethod
    def hex_to_time_slots(hex_str: str) -> List[int]:
        """Convert hexadecimal string to time slot list
        
        Args:
            hex_str (str): Hexadecimal string
            
        Returns:
            List[int]: List of time slot indices (1-16)
        """
        if not hex_str or hex_str == "0":
            return []
        
        try:
            value = int(hex_str, 16)
            slots = []
            
            for i in range(16):
                if value & (1 << i):
                    # Since bits are 0-15 and time slots are 1-16, need to add 1
                    slots.append(i + 1)
            
            return slots
        except ValueError:
            return []

    @staticmethod
    def shift_date(base_date: str, offset: int) -> str:
        """Get date after offset

        Args:
            base_date (str): Base date (YYYY-MM-DD)
            offset (int): Day offset, negative for earlier dates

        Returns:
            str: Date after offset
        """
        base = datetime.strptime(base_date, "%Y-%m-%d")
        new_date = base + timedelta(days=offset)
        return new_date.strftime("%Y-%m-%d")

    @staticmethod
    def get_current_datetime() -> datetime:
        """Get current datetime
        
        Returns:
            datetime: Current datetime
        """
        return datetime.now()
    
    @staticmethod
    def get_time_from_slot(time_slot: int) -> Tuple[int, int]:
        """Get hour and minute from time slot
        
        Args:
            time_slot (int): Time slot index (1-16)
            
        Returns:
            Tuple[int, int]: Hour (24-hour format) and minute
        """
        if time_slot < 1 or time_slot > 16:
            return (0, 0)
        
        # Time slots are from 9:00 AM to 5:00 PM in 30-minute increments
        hour = 9 + (time_slot - 1) // 2
        minute = 0 if (time_slot - 1) % 2 == 0 else 30
        
        return (hour, minute)
    
    @staticmethod
    def datetime_from_date_and_slot(date_str: str, time_slot: int) -> datetime:
        """Create datetime object from date string and time slot
        
        Args:
            date_str (str): Date in format "YYYY-MM-DD"
            time_slot (int): Time slot index (1-16)
            
        Returns:
            datetime: Datetime object
        """
        hour, minute = DateUtil.get_time_from_slot(time_slot)
        
        # Convert string date to datetime and set hour/minute
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return date_obj.replace(hour=hour, minute=minute, second=0, microsecond=0)
        except ValueError:
            # Return current time if date format is invalid
            return datetime.now()


# Test code
if __name__ == "__main__":
    # Date functionality test
    print("Current date:", DateUtil.get_current_date())
    
    today = DateUtil.get_current_date()
    tomorrow = DateUtil.get_date_range(today, 1)[1]
    print(f"Tomorrow: {tomorrow}")
    
    print(f"Is {tomorrow} a future date: {DateUtil.is_future_date(tomorrow)}")
    print(f"Day of week for {tomorrow}: {DateUtil.get_day_of_week(tomorrow)}")
    
    # Time slot functionality test
    print("\nTime slot string mappings:")
    for i in range(1, 17):
        time_slot_str = DateUtil.get_time_slot_str(i)
        print(f"Slot {i}: {time_slot_str}")
    
    # Example: Get time slot index from string
    test_time_str = "9:00 AM - 9:30 AM"
    time_slot = DateUtil.get_time_slot_from_str(test_time_str)
    print(f"\nTime slot for {test_time_str}: {time_slot}")
    
    # Example: Convert time slot list to hexadecimal string
    test_time_slots = [1, 5, 9, 13]
    hex_str = DateUtil.time_slots_to_hex(test_time_slots)
    print(f"\nTime slots {test_time_slots} converted to hexadecimal: {hex_str}")
    
    # Example: Convert hexadecimal string to time slot list
    test_hex_str = "0x1357"
    time_slots = DateUtil.hex_to_time_slots(test_hex_str)
    print(f"\nHexadecimal {test_hex_str} converted to time slots: {time_slots}") 
