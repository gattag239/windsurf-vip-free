"""
Utility functions for the Windsurf account registration program
"""
import os
import time
import shutil
import logging
import tkinter as tk
from tkinter import messagebox
import win32api
import win32con
import win32gui
from config import (
    CHROME_USER_DATA_DIR,
    CHROME_TEMP_DIR,
    CHROME_EXECUTABLE
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
    """Show message dialog"""
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    root.attributes('-topmost', True)  # 设置消息框总在最上层
    
    if type_ == "error":
        messagebox.showerror(title, message)
    elif type_ == "warning":
        messagebox.showwarning(title, message)
    elif type_ == "yesno":
        result = messagebox.askyesno(title, message)
        root.destroy()
        return result
    else:
        # 创建一个可以复制文本的对话框
        dialog = tk.Toplevel(root)
        dialog.title(title)
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.attributes('-topmost', True)
        
        # 添加文本框
        text = tk.Text(dialog, wrap=tk.WORD, padx=10, pady=10)
        text.insert(tk.END, message)
        text.pack(fill=tk.BOTH, expand=True)
        text.config(state="normal")  # 允许选择和复制
        
        # 添加复制按钮
        def copy_text():
            dialog.clipboard_clear()
            dialog.clipboard_append(message)
            dialog.update()
        
        copy_btn = tk.Button(dialog, text="复制内容", command=copy_text)
        copy_btn.pack(pady=5)
        
        # 添加确定按钮
        ok_btn = tk.Button(dialog, text="确定", command=dialog.destroy)
        ok_btn.pack(pady=5)
        
        # 设置焦点并等待
        dialog.focus_set()
        dialog.grab_set()
        dialog.wait_window()
    
    root.destroy()

def init_user_data():
    """初始化程序用户数据目录"""
    try:
        # 创建Chrome用户数据目录结构
        os.makedirs(CHROME_USER_DATA_DIR, exist_ok=True)
        os.makedirs(os.path.join(CHROME_USER_DATA_DIR, "Default"), exist_ok=True)
        os.makedirs(os.path.join(CHROME_USER_DATA_DIR, "Default", "Cache"), exist_ok=True)
        os.makedirs(os.path.join(CHROME_USER_DATA_DIR, "Default", "Code Cache"), exist_ok=True)
        
        # 创建Chrome临时目录
        os.makedirs(CHROME_TEMP_DIR, exist_ok=True)
        
        logging.info("程序用户数据目录初始化完成")
        return True
    except Exception as e:
        logging.error(f"初始化用户数据目录时出错: {e}")
        return False

def clean_chrome_dir(dir_path):
    """Clean Chrome directory"""
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path)
            logging.info(f"程序Chrome{os.path.basename(dir_path)}清理完成")
        except Exception as e:
            logging.error(f"清理Chrome{os.path.basename(dir_path)}时出错: {e}")

def clean_all_chrome_data():
    """Clean all Chrome related data"""
    clean_chrome_dir(CHROME_USER_DATA_DIR)
    clean_chrome_dir(CHROME_TEMP_DIR)

def set_english_ime():
    """设置英文输入法"""
    # 获取当前窗口句柄
    hwnd = win32gui.GetFocus()
    
    # 设置英文输入法
    im_list = win32api.GetKeyboardLayoutList()
    for im in im_list:
        if im & 0xFFFF == 0x0409:  # 英文输入法的ID
            win32api.SendMessage(
                hwnd,
                win32con.WM_INPUTLANGCHANGEREQUEST,
                0,
                im
            )
            break

def check_chrome_versions():
    """检查Chrome和ChromeDriver的版本"""
    try:
        # 检查Chrome版本
        chrome_version = ""
        if CHROME_EXECUTABLE and os.path.exists(CHROME_EXECUTABLE):
            try:
                import subprocess
                result = subprocess.run([CHROME_EXECUTABLE, '--version'], 
                                      capture_output=True, 
                                      text=True,
                                      creationflags=subprocess.CREATE_NO_WINDOW)
                if result.returncode == 0:
                    chrome_version = result.stdout.strip()
                    logging.info(f"Chrome版本: {chrome_version}")
                else:
                    logging.warning("无法获取Chrome版本")
            except Exception as e:
                logging.warning(f"检查Chrome版本时出错: {e}")
        else:
            logging.warning("未找到Chrome可执行文件")
        
        # 使用 webdriver_manager 获取 ChromeDriver 版本
        from webdriver_manager.chrome import ChromeDriverManager
        driver_path = ChromeDriverManager().install()
        driver_version = ""
        try:
            result = subprocess.run(['chromedriver', '--version'], 
                                  capture_output=True, 
                                  text=True,
                                  creationflags=subprocess.CREATE_NO_WINDOW)
            if result.returncode == 0:
                driver_version = result.stdout.strip()
                logging.info(f"ChromeDriver版本: {driver_version}")
            else:
                logging.warning("无法获取ChromeDriver版本")
        except Exception as e:
            logging.warning(f"检查ChromeDriver版本时出错: {e}")
        
        return chrome_version, driver_version
    except Exception as e:
        logging.error(f"检查版本时出错: {e}")
        return "", ""
