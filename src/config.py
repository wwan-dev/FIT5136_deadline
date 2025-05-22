#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Configuration file, defines system constants and configuration items
"""

# Time slot definitions, each time slot is 30 minutes
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

# Hexadecimal bit positions corresponding to time slots
# Example: 0x8000 indicates available only at 09:00-09:30
# 0xFFFF indicates available all day
# 0x0000 indicates not available all day
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

# Common time slot combinations
MORNING_SLOTS = 0xFC00  # 09:00-12:00
AFTERNOON_SLOTS = 0x03FF  # 13:00-18:00
ALL_DAY_SLOTS = 0xFFFF  # All day
NO_SLOTS = 0x0000  # Not available

# Appointment status
APPOINTMENT_STATUS = {
    "SCHEDULED": "Scheduled",
    "COMPLETED": "Completed",
    "CANCELLED_BY_PATIENT": "Cancelled by Patient",
    "CANCELLED_BY_CLINIC": "Cancelled by Clinic"
}

# Appointment reasons
APPOINTMENT_REASONS = {
    "GENERAL": "General Consultation",
    "VACCINATION": "Vaccination",
    "REFERRAL": "Referral",
    "CHRONIC": "Chronic Disease Management",
    "MENTAL": "Mental Health Consultation",
    "OTHER": "Other"
}

# Clinic service configuration
# Since the services field was removed from clinics.csv, define clinic services here
CLINIC_SERVICES = {
    1: ["General Consultation", "Vaccination", "Referral", "Chronic Disease Management", "Mental Health Consultation"],
    2: ["General Consultation", "Vaccination", "Referral", "Chronic Disease Management"],
    3: ["General Consultation", "Vaccination", "Mental Health Consultation"]
}

# Data file paths
DATA_DIR = "../data"
USERS_FILE = f"{DATA_DIR}/users.csv"
DOCTORS_FILE = f"{DATA_DIR}/doctors.csv"
CLINICS_FILE = f"{DATA_DIR}/clinics.csv"
APPOINTMENTS_FILE = f"{DATA_DIR}/appointments.csv"
DOCTOR_SCHEDULES_FILE = f"{DATA_DIR}/doctor_schedules.csv"
NOTIFICATIONS_FILE = f"{DATA_DIR}/notifications.csv"
APPOINTMENT_REASONS_FILE = f"{DATA_DIR}/appointment_reasons.csv"
