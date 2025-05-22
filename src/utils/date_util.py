#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日期和时间槽工具类，提供日期处理和时间槽转换功能
"""

import sys
import os
import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.config import TIME_SLOTS, HEX_TIME_SLOTS, MORNING_SLOTS, AFTERNOON_SLOTS, ALL_DAY_SLOTS, NO_SLOTS

class DateUtil:
    """日期和时间槽工具类"""
    
    # 日期格式常量
    DATE_FORMAT = "%Y-%m-%d"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    @staticmethod
    def get_current_date():
        """获取当前日期
        
        Returns:
            str: 当前日期字符串，格式为 "YYYY-MM-DD"
        """
        return datetime.datetime.now().strftime(DateUtil.DATE_FORMAT)
    
    @staticmethod
    def get_current_datetime():
        """获取当前日期时间
        
        Returns:
            str: 当前日期时间字符串，格式为 "YYYY-MM-DD HH:MM:SS"
        """
        return datetime.datetime.now().strftime(DateUtil.DATETIME_FORMAT)
    
    @staticmethod
    def parse_date(date_str):
        """解析日期字符串
        
        Args:
            date_str (str): 日期字符串，格式为 "YYYY-MM-DD"
            
        Returns:
            datetime.datetime: 日期对象
        """
        return datetime.datetime.strptime(date_str, DateUtil.DATE_FORMAT)
    
    @staticmethod
    def format_date(date_obj):
        """格式化日期对象
        
        Args:
            date_obj (datetime.datetime): 日期对象
            
        Returns:
            str: 日期字符串，格式为 "YYYY-MM-DD"
        """
        return date_obj.strftime(DateUtil.DATE_FORMAT)
    
    @staticmethod
    def add_days(date_str, days):
        """日期加上指定天数
        
        Args:
            date_str (str): 日期字符串，格式为 "YYYY-MM-DD"
            days (int): 要加上的天数
            
        Returns:
            str: 新的日期字符串，格式为 "YYYY-MM-DD"
        """
        date_obj = DateUtil.parse_date(date_str)
        new_date = date_obj + datetime.timedelta(days=days)
        return DateUtil.format_date(new_date)
    
    @staticmethod
    def days_between(date1_str, date2_str):
        """计算两个日期之间的天数
        
        Args:
            date1_str (str): 第一个日期字符串，格式为 "YYYY-MM-DD"
            date2_str (str): 第二个日期字符串，格式为 "YYYY-MM-DD"
            
        Returns:
            int: 两个日期之间的天数
        """
        date1 = DateUtil.parse_date(date1_str)
        date2 = DateUtil.parse_date(date2_str)
        delta = date2 - date1
        return abs(delta.days)
    
    @staticmethod
    def is_future_date(date_str):
        """检查日期是否是未来日期
        
        Args:
            date_str (str): 日期字符串，格式为 "YYYY-MM-DD"
            
        Returns:
            bool: 如果是未来日期返回True，否则返回False
        """
        date_obj = DateUtil.parse_date(date_str)
        today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return date_obj > today
    
    @staticmethod
    def is_valid_appointment_date(date_str):
        """检查日期是否是有效的预约日期（至少是当前日期之后的2小时）
        
        Args:
            date_str (str): 日期字符串，格式为 "YYYY-MM-DD"
            
        Returns:
            bool: 如果是有效的预约日期返回True，否则返回False
        """
        date_obj = DateUtil.parse_date(date_str)
        now = datetime.datetime.now()
        min_appointment_time = now + datetime.timedelta(hours=2)
        return date_obj.date() > now.date() or (date_obj.date() == now.date() and min_appointment_time.time() <= now.time())
    
    @staticmethod
    def get_weekday(date_str):
        """获取日期的星期几
        
        Args:
            date_str (str): 日期字符串，格式为 "YYYY-MM-DD"
            
        Returns:
            int: 星期几（0-6，0表示星期一）
        """
        date_obj = DateUtil.parse_date(date_str)
        return date_obj.weekday()
    
    @staticmethod
    def get_weekday_name(date_str):
        """获取日期的星期几名称
        
        Args:
            date_str (str): 日期字符串，格式为 "YYYY-MM-DD"
            
        Returns:
            str: 星期几的名称
        """
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        weekday = DateUtil.get_weekday(date_str)
        return weekdays[weekday]
    
    # 以下是从TimeSlotUtils移植过来的方法
    
    @staticmethod
    def get_time_range(slot_index):
        """获取时间槽对应的具体时间范围
        
        Args:
            slot_index (int): 时间槽索引（0-15）
            
        Returns:
            str: 时间范围字符串，如 "09:00-09:30"
        """
        if slot_index < 0 or slot_index > 15:
            raise ValueError("时间槽索引必须在0-15之间")
        
        return TIME_SLOTS[slot_index]
    
    @staticmethod
    def get_hex_mask(slot_index):
        """获取时间槽对应的16进制掩码
        
        Args:
            slot_index (int): 时间槽索引（0-15）
            
        Returns:
            int: 16进制掩码值
        """
        if slot_index < 0 or slot_index > 15:
            raise ValueError("时间槽索引必须在0-15之间")
        
        return HEX_TIME_SLOTS[slot_index]
    
    @staticmethod
    def is_slot_available(hex_slots, slot_index):
        """检查指定的时间槽是否可用
        
        Args:
            hex_slots (int): 16进制表示的时间槽
            slot_index (int): 要检查的时间槽索引（0-15）
            
        Returns:
            bool: 如果时间槽可用返回True，否则返回False
        """
        mask = DateUtil.get_hex_mask(slot_index)
        return (int(hex_slots, 16) & mask) != 0
    
    @staticmethod
    def get_available_slots(hex_slots):
        """获取所有可用的时间槽索引列表
        
        Args:
            hex_slots (int): 16进制表示的时间槽
            
        Returns:
            list: 可用时间槽索引列表
        """
        available_slots = []
        hex_value = int(hex_slots, 16)
        
        for i in range(16):
            mask = DateUtil.get_hex_mask(i)
            if (hex_value & mask) != 0:
                available_slots.append(i)
                
        return available_slots
    
    @staticmethod
    def get_available_time_ranges(hex_slots):
        """获取所有可用的时间范围列表
        
        Args:
            hex_slots (int): 16进制表示的时间槽
            
        Returns:
            list: 可用时间范围字符串列表
        """
        available_slots = DateUtil.get_available_slots(hex_slots)
        return [TIME_SLOTS[slot] for slot in available_slots]
    
    @staticmethod
    def reserve_slot(hex_slots, slot_index):
        """预约指定的时间槽（将对应位置为0）
        
        Args:
            hex_slots (str): 16进制表示的时间槽
            slot_index (int): 要预约的时间槽索引（0-15）
            
        Returns:
            str: 更新后的16进制时间槽
        """
        mask = ~DateUtil.get_hex_mask(slot_index)
        new_slots = int(hex_slots, 16) & mask
        return hex(new_slots)[2:].zfill(4)  # 确保输出是4位长度的16进制字符串
    
    @staticmethod
    def release_slot(hex_slots, slot_index):
        """释放指定的时间槽（将对应位置为1）
        
        Args:
            hex_slots (str): 16进制表示的时间槽
            slot_index (int): 要释放的时间槽索引（0-15）
            
        Returns:
            str: 更新后的16进制时间槽
        """
        mask = DateUtil.get_hex_mask(slot_index)
        new_slots = int(hex_slots, 16) | mask
        return hex(new_slots)[2:].zfill(4)  # 确保输出是4位长度的16进制字符串
    
    @staticmethod
    def check_slot_conflict(doctor_schedules, doctor_id, date, slot_index):
        """检查医生在指定日期和时间槽是否有冲突预约
        
        Args:
            doctor_schedules (list): 医生排班记录列表
            doctor_id (int): 医生ID
            date (str): 日期字符串，格式为 "YYYY-MM-DD"
            slot_index (int): 时间槽索引（0-15）
            
        Returns:
            bool: 如果有冲突返回True，否则返回False
        """
        for schedule in doctor_schedules:
            if schedule['doctor_id'] == doctor_id and schedule['date'] == date:
                # 检查该医生在这个日期的所有诊所排班
                if DateUtil.is_slot_available(schedule['time_slots'], slot_index):
                    # 该医生在此时间槽已有排班
                    return True
        
        return False


# 测试代码
if __name__ == "__main__":
    # 日期相关功能测试
    print("当前日期:", DateUtil.get_current_date())
    print("当前日期时间:", DateUtil.get_current_datetime())
    
    today = DateUtil.get_current_date()
    tomorrow = DateUtil.add_days(today, 1)
    print(f"明天: {tomorrow}")
    
    days = DateUtil.days_between(today, tomorrow)
    print(f"{today} 和 {tomorrow} 之间相差 {days} 天")
    
    print(f"{tomorrow} 是否是未来日期: {DateUtil.is_future_date(tomorrow)}")
    print(f"{tomorrow} 是星期几: {DateUtil.get_weekday_name(tomorrow)}")
    
    # 时间槽相关功能测试
    print("\n时间槽与16进制掩码对应关系：")
    for i in range(16):
        time_range = DateUtil.get_time_range(i)
        hex_mask = hex(DateUtil.get_hex_mask(i))
        print(f"槽位 {i}: {time_range} -> 掩码: {hex_mask}")
    
    # 示例：检查某个16进制数中哪些时间槽可用
    test_slots = "0xF0F0"
    print(f"\n时间槽 {test_slots} 中可用的槽位:")
    available_slots = DateUtil.get_available_slots(test_slots)
    for slot in available_slots:
        print(f"槽位 {slot}: {DateUtil.get_time_range(slot)}")
    
    # 示例：预约和释放时间槽
    test_slots = "0xFFFF"  # 所有槽位都可用
    print(f"\n初始槽位: {test_slots}")
    
    # 预约槽位0（09:00-09:30）
    reserved = DateUtil.reserve_slot(test_slots, 0)
    print(f"预约槽位0后: 0x{reserved}")
    
    # 再释放槽位0
    released = DateUtil.release_slot(reserved, 0)
    print(f"释放槽位0后: 0x{released}") 
