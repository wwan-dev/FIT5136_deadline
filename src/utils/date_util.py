#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日期工具类，提供日期和时间槽相关的操作
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class DateUtil:
    """日期工具类，提供日期和时间槽相关的操作"""
    
    # 时间槽映射，每个时间槽对应半小时
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
        """获取时间槽的字符串表示
        
        Args:
            time_slot (int): 时间槽索引（1-16）
            
        Returns:
            str: 时间槽的字符串表示
        """
        if time_slot in DateUtil.TIME_SLOT_MAP:
            return DateUtil.TIME_SLOT_MAP[time_slot]
        return "Unknown Time Slot"
    
    @staticmethod
    def get_time_slot_from_str(time_str: str) -> int:
        """从字符串获取时间槽索引
        
        Args:
            time_str (str): 时间字符串
            
        Returns:
            int: 时间槽索引（1-16），如果不匹配则返回0
        """
        for slot, slot_str in DateUtil.TIME_SLOT_MAP.items():
            if slot_str == time_str:
                return slot
        return 0
    
    @staticmethod
    def get_current_date() -> str:
        """获取当前日期
        
        Returns:
            str: 当前日期，格式为 "YYYY-MM-DD"
        """
        return datetime.now().strftime("%Y-%m-%d")
    
    @staticmethod
    def get_date_range(start_date: str, days: int) -> List[str]:
        """获取日期范围
        
        Args:
            start_date (str): 开始日期，格式为 "YYYY-MM-DD"
            days (int): 天数
            
        Returns:
            List[str]: 日期列表
        """
        start = datetime.strptime(start_date, "%Y-%m-%d")
        date_list = []
        
        for i in range(days):
            date = start + timedelta(days=i)
            date_list.append(date.strftime("%Y-%m-%d"))
        
        return date_list
    
    @staticmethod
    def is_future_date(date_str: str) -> bool:
        """判断日期是否是未来日期
        
        Args:
            date_str (str): 日期，格式为 "YYYY-MM-DD"
            
        Returns:
            bool: 如果是未来日期返回True，否则返回False
        """
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            today = datetime.now().date()
            return date > today
        except ValueError:
            return False
    
    @staticmethod
    def is_valid_date(date_str: str) -> bool:
        """判断日期是否有效
        
        Args:
            date_str (str): 日期，格式为 "YYYY-MM-DD"
            
        Returns:
            bool: 如果日期有效返回True，否则返回False
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def format_date(date_str: str, input_format: str = "%Y-%m-%d", output_format: str = "%d/%m/%Y") -> str:
        """格式化日期
        
        Args:
            date_str (str): 日期字符串
            input_format (str, optional): 输入格式. 默认为 "%Y-%m-%d".
            output_format (str, optional): 输出格式. 默认为 "%d/%m/%Y".
            
        Returns:
            str: 格式化后的日期字符串
        """
        try:
            date = datetime.strptime(date_str, input_format)
            return date.strftime(output_format)
        except ValueError:
            return date_str
    
    @staticmethod
    def get_day_of_week(date_str: str) -> str:
        """获取星期几
        
        Args:
            date_str (str): 日期，格式为 "YYYY-MM-DD"
            
        Returns:
            str: 星期几
        """
        try:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            return days[date.weekday()]
        except ValueError:
            return "Unknown"
    
    @staticmethod
    def time_slots_to_hex(time_slots: List[int]) -> str:
        """将时间槽列表转换为16进制字符串
        
        Args:
            time_slots (List[int]): 时间槽索引列表（1-16）
            
        Returns:
            str: 16进制字符串
        """
        if not time_slots:
            return "0"
        
        value = 0
        for slot in time_slots:
            if 1 <= slot <= 16:
                # 由于时间槽是1-16，而位是0-15，需要减1
                value |= (1 << (slot - 1))
        
        return format(value, 'x')
    
    @staticmethod
    def hex_to_time_slots(hex_str: str) -> List[int]:
        """将16进制字符串转换为时间槽列表
        
        Args:
            hex_str (str): 16进制字符串
            
        Returns:
            List[int]: 时间槽索引列表（1-16）
        """
        if not hex_str or hex_str == "0":
            return []
        
        try:
            value = int(hex_str, 16)
            slots = []
            
            for i in range(16):
                if value & (1 << i):
                    # 由于位是0-15，而时间槽是1-16，需要加1
                    slots.append(i + 1)
            
            return slots
        except ValueError:
            return []


# 测试代码
if __name__ == "__main__":
    # 日期相关功能测试
    print("当前日期:", DateUtil.get_current_date())
    
    today = DateUtil.get_current_date()
    tomorrow = DateUtil.get_date_range(today, 1)[1]
    print(f"明天: {tomorrow}")
    
    print(f"{tomorrow} 是否是未来日期: {DateUtil.is_future_date(tomorrow)}")
    print(f"{tomorrow} 是星期几: {DateUtil.get_day_of_week(tomorrow)}")
    
    # 时间槽相关功能测试
    print("\n时间槽与字符串对应关系：")
    for i in range(1, 17):
        time_slot_str = DateUtil.get_time_slot_str(i)
        print(f"槽位 {i}: {time_slot_str}")
    
    # 示例：从字符串获取时间槽索引
    test_time_str = "9:00 AM - 9:30 AM"
    time_slot = DateUtil.get_time_slot_from_str(test_time_str)
    print(f"\n时间槽 {test_time_str} 对应的槽位: {time_slot}")
    
    # 示例：将时间槽列表转换为16进制字符串
    test_time_slots = [1, 5, 9, 13]
    hex_str = DateUtil.time_slots_to_hex(test_time_slots)
    print(f"\n时间槽 {test_time_slots} 转换为16进制字符串: {hex_str}")
    
    # 示例：将16进制字符串转换为时间槽列表
    test_hex_str = "0x1357"
    time_slots = DateUtil.hex_to_time_slots(test_hex_str)
    print(f"\n16进制字符串 {test_hex_str} 转换为时间槽: {time_slots}") 
