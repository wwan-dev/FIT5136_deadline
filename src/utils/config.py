"""
配置文件，包含系统所需的静态数据
"""

# 文件路径配置
DATA_PATH = "../data/"
PATIENTS_FILE = DATA_PATH + "patients.csv"
DOCTORS_FILE = DATA_PATH + "doctors.csv"
DEPARTMENTS_FILE = DATA_PATH + "departments.csv"
APPOINTMENTS_FILE = DATA_PATH + "appointments.csv"

# 系统用户配置
DEFAULT_PATIENTS = [
    {"email": "patient1@student.monash.edu", "password": "Monash1234!", "role": "patient"},
    {"email": "patient2@student.monash.edu", "password": "Monash1234!", "role": "patient"}
]

DEFAULT_ADMIN = {"email": "admin@monash.edu", "password": "Admin1234!", "role": "admin"}

# 时间槽配置（8小时工作制，16个时间槽，每个30分钟）
TIME_SLOTS = [
    "08:00-08:30", "08:30-09:00", "09:00-09:30", "09:30-10:00",
    "10:00-10:30", "10:30-11:00", "11:00-11:30", "11:30-12:00",
    "13:00-13:30", "13:30-14:00", "14:00-14:30", "14:30-15:00",
    "15:00-15:30", "15:30-16:00", "16:00-16:30", "16:30-17:00"
]

# 预约原因类型
APPOINTMENT_REASONS = [
    "一般体检", 
    "疫苗接种", 
    "专科转诊", 
    "慢性疾病管理", 
    "心理健康咨询",
    "其他"
]

# 预约状态类型
APPOINTMENT_STATUS = [
    "已预约",
    "已到诊",
    "患者取消",
    "诊所取消"
]

# 医生预约时长配置（分钟）
APPOINTMENT_DURATIONS = [15, 25, 40, 60] 
