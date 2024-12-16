"""
Utility functions for the Windsurf account registration program
"""
import os
import time
import shutil
import logging
import tkinter as tk
from tkinter import messagebox
from config import (
    CHROME_USER_DATA_DIR,
    CHROME_TEMP_DIR,
    CHROME_EXECUTABLE,
    CHROME_DRIVER
)

def format_email(prefix, number, domain):
    """Format email address with number"""
    try:
        num = int(number)
        return f"{prefix}{num}@{domain}"
    except (ValueError, TypeError):
        return f"{prefix}{number}@{domain}"

def center_window(window):
    """Center a tkinter window on the screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def show_message(title, message, type_="info"):
    """Show message box with specified type"""
    if type_ == "yesno":
        return messagebox.askyesno(title, message)
    elif type_ == "error":
        messagebox.showerror(title, message)
    else:
        # 创建一个可以复制文本的对话框
        dialog = tk.Toplevel()
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)
        
        # 添加文本框
        text = tk.Text(dialog, wrap=tk.WORD, padx=10, pady=10)
        text.insert(tk.END, message)
        text.pack(fill=tk.BOTH, expand=True)
        text.config(state="normal")  # 允许选择和复制
        
        # 添加确定按钮
        button = tk.Button(dialog, text="确定", command=dialog.destroy)
        button.pack(pady=10)
        
        # 设置焦点并等待
        dialog.focus_set()
        dialog.grab_set()
        dialog.wait_window()

def clean_all_chrome_data():
    """Clean all Chrome user data"""
    try:
        # 先尝试结束Chrome进程
        try:
            import subprocess
            subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], 
                         capture_output=True, 
                         creationflags=subprocess.CREATE_NO_WINDOW)
            logging.info("已结束Chrome进程")
        except Exception as e:
            logging.warning(f"结束Chrome进程时出错: {e}")
        
        # 等待进程结束
        time.sleep(1)
        
        # 清理Chrome用户数据目录
        if os.path.exists(CHROME_USER_DATA_DIR):
            try:
                shutil.rmtree(CHROME_USER_DATA_DIR)
                os.makedirs(CHROME_USER_DATA_DIR)
                logging.info("Chrome用户数据目录清理完成")
            except Exception as e:
                logging.error(f"清理用户数据目录时出错: {e}")
        
        # 清理Chrome临时目录
        if os.path.exists(CHROME_TEMP_DIR):
            try:
                shutil.rmtree(CHROME_TEMP_DIR)
                os.makedirs(CHROME_TEMP_DIR)
                logging.info("Chrome临时目录清理完成")
            except Exception as e:
                logging.error(f"清理临时目录时出错: {e}")
        
    except Exception as e:
        logging.error(f"清理Chrome数据时出错: {e}")

def check_chrome_versions():
    """检查Chrome和ChromeDriver的版本"""
    try:
        # 检查Chrome版本
        chrome_version = ""
        try:
            result = subprocess.run([CHROME_EXECUTABLE, '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            chrome_version = result.stdout.strip()
            logging.info(f"Chrome版本: {chrome_version}")
        except Exception as e:
            logging.error(f"获取Chrome版本失败: {e}")
        
        # 检查ChromeDriver版本
        driver_version = ""
        try:
            result = subprocess.run([CHROME_DRIVER, '--version'], 
                                  capture_output=True, 
                                  text=True,
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            driver_version = result.stdout.strip()
            logging.info(f"ChromeDriver版本: {driver_version}")
        except Exception as e:
            logging.error(f"获取ChromeDriver版本失败: {e}")
        
        # 提取版本号
        chrome_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', chrome_version)
        driver_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', driver_version)
        
        if chrome_match and driver_match:
            chrome_ver = chrome_match.group(1)
            driver_ver = driver_match.group(1)
            
            # 比较主版本号
            chrome_major = chrome_ver.split('.')[0]
            driver_major = driver_ver.split('.')[0]
            
            if chrome_major == driver_major:
                logging.info("Chrome和ChromeDriver版本匹配")
                return True
            else:
                logging.error(f"版本不匹配！Chrome主版本: {chrome_major}, ChromeDriver主版本: {driver_major}")
                return False
        else:
            logging.error("无法解析版本号")
            return False
            
    except Exception as e:
        logging.error(f"检查版本时出错: {e}")
        return False
