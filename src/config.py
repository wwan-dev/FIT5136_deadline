#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置文件，定义系统常量和配置项
"""

# 时间槽定义，每个时间槽30分钟
TIME_SLOTS = {
    0: "09:00-09:30",
    1: "09:30-10:00",
    2: "10:00-10:30",
    3: "10:30-11:00",
    4: "11:00-11:30",
    5: "11:30-12:00",
    6: "13:00-13:30",
    7: "13:30-14:00",
    8: "14:00-14:30",
    9: "14:30-15:00",
    10: "15:00-15:30",
    11: "15:30-16:00",
    12: "16:00-16:30",
    13: "16:30-17:00",
    14: "17:00-17:30",
    15: "17:30-18:00"
}

# 16进制数位对应的时间槽
# 例如：0x8000 表示只在09:00-09:30时间段坐诊
# 0xFFFF 表示全天坐诊
# 0x0000 表示全天不坐诊
HEX_TIME_SLOTS = {
    0: 0x8000,  # 09:00-09:30
    1: 0x4000,  # 09:30-10:00
    2: 0x2000,  # 10:00-10:30
    3: 0x1000,  # 10:30-11:00
    4: 0x0800,  # 11:00-11:30
    5: 0x0400,  # 11:30-12:00
    6: 0x0200,  # 13:00-13:30
    7: 0x0100,  # 13:30-14:00
    8: 0x0080,  # 14:00-14:30
    9: 0x0040,  # 14:30-15:00
    10: 0x0020,  # 15:00-15:30
    11: 0x0010,  # 15:30-16:00
    12: 0x0008,  # 16:00-16:30
    13: 0x0004,  # 16:30-17:00
    14: 0x0002,  # 17:00-17:30
    15: 0x0001   # 17:30-18:00
}

# 常用时间槽组合
MORNING_SLOTS = 0xFC00  # 09:00-12:00
AFTERNOON_SLOTS = 0x03FF  # 13:00-18:00
ALL_DAY_SLOTS = 0xFFFF  # 全天
NO_SLOTS = 0x0000  # 不坐诊

# 预约状态
APPOINTMENT_STATUS = {
    "SCHEDULED": "Scheduled",
    "COMPLETED": "Completed",
    "CANCELLED_BY_PATIENT": "Cancelled by Patient",
    "CANCELLED_BY_CLINIC": "Cancelled by Clinic"
}

# 预约原因
APPOINTMENT_REASONS = {
    "GENERAL": "General Consultation",
    "VACCINATION": "Vaccination",
    "REFERRAL": "Referral",
    "CHRONIC": "Chronic Disease Management",
    "MENTAL": "Mental Health Consultation",
    "OTHER": "Other"
}

# 诊所服务配置
# 由于services字段从clinics.csv中移除，在这里定义诊所提供的服务
CLINIC_SERVICES = {
    1: ["General Consultation", "Vaccination", "Referral", "Chronic Disease Management", "Mental Health Consultation"],
    2: ["General Consultation", "Vaccination", "Referral", "Chronic Disease Management"],
    3: ["General Consultation", "Vaccination", "Mental Health Consultation"]
}

# 数据文件路径
DATA_DIR = "../data"
USERS_FILE = f"{DATA_DIR}/users.csv"
DOCTORS_FILE = f"{DATA_DIR}/doctors.csv"
CLINICS_FILE = f"{DATA_DIR}/clinics.csv"
APPOINTMENTS_FILE = f"{DATA_DIR}/appointments.csv"
DOCTOR_SCHEDULES_FILE = f"{DATA_DIR}/doctor_schedules.csv"
NOTIFICATIONS_FILE = f"{DATA_DIR}/notifications.csv"
APPOINTMENT_REASONS_FILE = f"{DATA_DIR}/appointment_reasons.csv"
