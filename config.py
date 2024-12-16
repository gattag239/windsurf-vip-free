"""
Configuration module for the Windsurf account registration program
"""
import os
import logging
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import ctypes

# GUI settings
WINDOW_TITLE = "Windsurf账号注册工具（无限使用pro用户功能）"
WINDOW_WIDTH = 990
WINDOW_HEIGHT = 1300
WINDOW_GEOMETRY = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+100+100"  # 设置窗口位置在屏幕左上角

# Default values
DEFAULT_EMAIL_PREFIX = "windsurf"
DEFAULT_EMAIL_DOMAIN = "2925.com"
DEFAULT_PASSWORD = "asdf1234"

# Email domains
EMAIL_DOMAINS = [
    "2925.com",
    "gmail.com"
]

# 项目根目录
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Chrome settings
CHROME_EXECUTABLE = os.path.join(ROOT_DIR, "chrome", "chrome.exe")
CHROME_DRIVER = os.path.join(ROOT_DIR, "chrome", "chromedriver.exe")

# Chrome user data directory
CHROME_USER_DATA_DIR = os.path.join(ROOT_DIR, "chrome", "userdata")
CHROME_TEMP_DIR = os.path.join(ROOT_DIR, "chrome", "temp")

# 确保目录存在
os.makedirs(os.path.dirname(CHROME_EXECUTABLE), exist_ok=True)
os.makedirs(CHROME_USER_DATA_DIR, exist_ok=True)
os.makedirs(CHROME_TEMP_DIR, exist_ok=True)

# 检查必要文件
if not os.path.exists(CHROME_EXECUTABLE):
    logging.error(f"Chrome可执行文件不存在: {CHROME_EXECUTABLE}")
if not os.path.exists(CHROME_DRIVER):
    logging.error(f"ChromeDriver不存在: {CHROME_DRIVER}")

# URLs
REGISTER_URL = "https://codeium.com/account/register"
PROFILE_URL = "https://codeium.com/profile"
ONBOARDING_NAME_URL = "https://codeium.com/account/onboarding?page=name"
ONBOARDING_ABOUT_URL = "https://codeium.com/account/onboarding?page=about"
ONBOARDING_SOURCE_URL = "https://codeium.com/account/onboarding?page=source"

# Timeouts
PAGE_LOAD_TIMEOUT = 30  # 页面加载超时时间
ELEMENT_WAIT_TIMEOUT = 20  # 元素等待超时时间
RETRY_INTERVAL = 2  # 重试间隔时间

# Log settings
LOG_FILE = os.path.join(ROOT_DIR, 'output.log')  
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
