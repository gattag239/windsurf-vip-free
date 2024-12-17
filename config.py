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
import winreg

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

def get_chrome_path():
    """获取Chrome路径，优先使用项目目录下的Chrome"""
    # 首先检查项目目录下的Chrome
    project_chrome = os.path.join(ROOT_DIR, "chrome", "chrome.exe")
    if os.path.exists(project_chrome):
        return project_chrome

    # 如果项目目录下没有，再尝试从注册表获取Chrome安装路径
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe")
        chrome_path = winreg.QueryValue(key, None)
        winreg.CloseKey(key)
        if os.path.exists(chrome_path):
            return chrome_path
    except WindowsError:
        pass

    # 检查常见安装位置
    common_locations = [
        os.path.expandvars("%ProgramFiles%\\Google\\Chrome\\Application\\chrome.exe"),
        os.path.expandvars("%ProgramFiles(x86)%\\Google\\Chrome\\Application\\chrome.exe"),
        os.path.expandvars("%LocalAppData%\\Google\\Chrome\\Application\\chrome.exe")
    ]
    
    for location in common_locations:
        if os.path.exists(location):
            return location
            
    return None

def get_chrome_version():
    """获取Chrome版本号"""
    try:
        # 尝试从注册表获取版本号
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
            version = winreg.QueryValueEx(key, "version")[0]
            winreg.CloseKey(key)
            return version
        except WindowsError:
            pass

        # 如果注册表方法失败，尝试从安装目录获取版本号
        chrome_path = get_chrome_path()
        if chrome_path:
            import os
            version_file = os.path.join(os.path.dirname(chrome_path), "chrome.VisualElementsManifest.xml")
            if os.path.exists(version_file):
                import xml.etree.ElementTree as ET
                tree = ET.parse(version_file)
                root = tree.getroot()
                version = root.attrib.get('Version', '')
                if version:
                    return version
    except:
        pass
    return None

def get_project_chromedriver_path():
    """获取项目目录下的ChromeDriver路径"""
    driver_path = os.path.join(ROOT_DIR, "chrome", "chromedriver.exe")
    return driver_path if os.path.exists(driver_path) else None

# Chrome settings
CHROME_EXECUTABLE = get_chrome_path()
CHROME_VERSION = get_chrome_version()
PROJECT_CHROMEDRIVER = get_project_chromedriver_path()

# Chrome driver path
CHROME_DRIVER = os.path.join(ROOT_DIR, "chrome", "chromedriver.exe")

# Chrome user data directory
CHROME_USER_DATA_DIR = os.path.join(ROOT_DIR, "userdata")
CHROME_TEMP_DIR = os.path.join(ROOT_DIR, "temp")

# 日志配置
LOG_DIR = os.path.join(ROOT_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "windsurf.log")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# 确保目录存在
os.makedirs(CHROME_USER_DATA_DIR, exist_ok=True)
os.makedirs(CHROME_TEMP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# URLs
REGISTER_URL = "https://codeium.com/account/register"
PROFILE_URL = "https://codeium.com/profile"
ONBOARDING_NAME_URL = "https://codeium.com/onboarding/name"
ONBOARDING_ABOUT_URL = "https://codeium.com/onboarding/about-user"
ONBOARDING_SOURCE_URL = "https://codeium.com/account/onboarding/source"

# Timeouts
PAGE_LOAD_TIMEOUT = 300  # 增加页面加载超时时间到5分钟
ELEMENT_WAIT_TIMEOUT = 30  # 增加元素等待时间到30秒
RETRY_INTERVAL = 1  # 每秒检查一次
