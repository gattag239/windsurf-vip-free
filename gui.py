"""
GUI module for the Windsurf account registration program
"""
import tkinter as tk
import ttkbootstrap as ttkb
from config import (
    WINDOW_TITLE,
    WINDOW_GEOMETRY,
    DEFAULT_EMAIL_PREFIX,
    DEFAULT_EMAIL_DOMAIN,
    DEFAULT_PASSWORD,
    EMAIL_DOMAINS
)
from utils import format_email
from logger import setup_logger
from tkinter import messagebox
import webbrowser

class RegistrationGUI:
    def __init__(self, register_callback):
        self.register_callback = register_callback
        
        # Create main window
        self.root = ttkb.Window(title=WINDOW_TITLE)
        self.root.geometry(WINDOW_GEOMETRY)  # 设置窗口位置
        self.root.resizable(True, True)  # 允许调整窗口大小
        self.root.attributes('-topmost', False)  # 取消窗口置顶
        
        # Configure grid
        for i in range(6):
            self.root.grid_columnconfigure(i, weight=1)
        self.root.grid_rowconfigure(8, weight=1)  # Make log display expandable
        
        # Create main frame with padding
        self.main_frame = ttkb.Frame(self.root, padding=20)
        self.main_frame.grid(row=0, column=0, columnspan=6, sticky="nsew")
        
        # Create widgets
        self.create_widgets()
        
        # Setup logger
        self.logger = setup_logger(self.log_display)
        
    def create_widgets(self):
        # Title
        title = ttkb.Label(
            self.main_frame,
            text=WINDOW_TITLE,
            bootstyle="primary",
            font=("", 20, "bold")
        )
        title.grid(row=0, column=0, columnspan=6, pady=(0, 20))
        
        # Headless mode
        self.headless_var = tk.BooleanVar(value=True)  # 默认显示浏览器
        headless_check = ttkb.Checkbutton(
            self.main_frame,
            text="显示创建过程",
            variable=self.headless_var,
            bootstyle="primary-round-toggle"
        )
        headless_check.grid(row=1, column=0, columnspan=6, pady=(0, 20))
        
        # Email settings frame
        email_frame = ttkb.Labelframe(self.main_frame, text="邮箱设置", padding=10)
        email_frame.grid(row=2, column=0, columnspan=6, sticky="ew", pady=(0, 20))
        
        # - Email prefix
        ttkb.Label(email_frame, text="主邮箱用户名：").grid(row=0, column=0, padx=5, pady=5)
        self.email_prefix = ttkb.Entry(email_frame, width=20)
        self.email_prefix.insert(0, DEFAULT_EMAIL_PREFIX)
        self.email_prefix.grid(row=0, column=1, padx=5, pady=5)
        
        # - Email number
        ttkb.Label(email_frame, text="序号：").grid(row=0, column=2, padx=5, pady=5)
        self.email_number = ttkb.Entry(email_frame, width=10)
        self.email_number.insert(0, "1")
        self.email_number.grid(row=0, column=3, padx=5, pady=5)
        
        # - Email domain
        ttkb.Label(email_frame, text="邮箱类型：").grid(row=0, column=4, padx=5, pady=5)
        self.email_domain = ttkb.Combobox(
            email_frame,
            values=EMAIL_DOMAINS,
            state="readonly",
            width=15
        )
        self.email_domain.set(DEFAULT_EMAIL_DOMAIN)
        self.email_domain.grid(row=0, column=5, padx=5, pady=5)
        
        # Email preview
        preview_frame = ttkb.Labelframe(self.main_frame, text="账号预览", padding=10)
        preview_frame.grid(row=3, column=0, columnspan=6, sticky="ew", pady=(0, 20))
        
        ttkb.Label(preview_frame, text="拟注册账号：").grid(row=0, column=0, padx=5, pady=5)
        self.account_preview = ttkb.Entry(preview_frame, state="readonly", width=40)
        self.account_preview.grid(row=0, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        # Password frame
        password_frame = ttkb.Labelframe(self.main_frame, text="密码设置", padding=10)
        password_frame.grid(row=4, column=0, columnspan=6, sticky="ew", pady=(0, 20))
        
        ttkb.Label(password_frame, text="注册密码：").grid(row=0, column=0, padx=5, pady=5)
        self.password = ttkb.Entry(password_frame, show="*", width=20)
        self.password.insert(0, DEFAULT_PASSWORD)
        self.password.grid(row=0, column=1, padx=5, pady=5)
        
        # Show password
        self.show_password_var = tk.BooleanVar()
        show_password = ttkb.Checkbutton(
            password_frame,
            text="显示密码",
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
            bootstyle="primary-round-toggle"
        )
        show_password.grid(row=0, column=2, padx=5, pady=5)
        
        # Buttons
        button_frame = ttkb.Frame(self.main_frame)
        button_frame.grid(row=5, column=0, columnspan=6, pady=(0, 20))
        
        self.next_button = ttkb.Button(
            button_frame,
            text="下一步",
            command=self.on_next,
            bootstyle="primary",
            width=15
        )
        self.next_button.pack(side="left", padx=10)
        
        self.close_button = ttkb.Button(
            button_frame,
            text="关闭",
            command=self.root.destroy,
            bootstyle="secondary",
            width=15
        )
        self.close_button.pack(side="left", padx=10)
        
        # Usage instructions
        usage_frame = ttkb.Labelframe(self.main_frame, text="使用说明", padding=10)
        usage_frame.grid(row=6, column=0, columnspan=6, sticky="ew", pady=(0, 20))
        
        usage_text = ttkb.Text(usage_frame, height=5, state="normal", wrap="word")
        usage_text.insert("1.0",
            "1. 输入主邮箱用户名（默认：windsurf，请务必进行修改）\n"
            "2. 输入序号（1-999999）\n"
            "3. 选择邮箱类型（支持2925.com和gmail.com）\n"
            "4. 确认密码（默认：asdf1234）\n"
            "5. 点击下一步开始注册流程"
        )
        usage_text.configure(state="disabled")
        usage_text.pack(fill="both", expand=True)
        
        # Log display
        log_frame = ttkb.Labelframe(self.main_frame, text="运行日志", padding=10)
        log_frame.grid(row=8, column=0, columnspan=6, sticky="nsew", pady=(0, 20))
        log_frame.grid_rowconfigure(0, weight=1)
        log_frame.grid_columnconfigure(0, weight=1)
        
        self.log_display = ttkb.Text(
            log_frame,
            height=20,  # 增加日志显示区域高度
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.log_display.grid(row=0, column=0, sticky="nsew")
        
        # Add scrollbar
        scrollbar = ttkb.Scrollbar(
            log_frame,
            orient="vertical",
            command=self.log_display.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.log_display["yscrollcommand"] = scrollbar.set
        
        # Author info with clickable link
        author_label = ttkb.Label(
            self.main_frame,
            text="作者：jayleehappy",
            bootstyle="primary",  # 改为primary样式，颜色更明显
            font=("", 10, "bold")  # 增加字体大小并加粗
        )
        author_label.grid(row=7, column=0, columnspan=3)
        
        # GitHub link
        github_link = ttkb.Label(
            self.main_frame,
            text="访问项目github",
            bootstyle="primary",  # 改为primary样式，颜色更明显
            cursor="hand2",
            font=("", 10, "bold", "underline")  # 增加字体大小并加粗
        )
        github_link.grid(row=7, column=3, columnspan=3)
        github_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/jayleehappy/windsurf-vip-free"))
        
        # Bind events
        self.email_prefix.bind("<KeyRelease>", lambda e: self.update_preview())
        self.email_number.bind("<KeyRelease>", lambda e: self.update_preview())
        self.email_domain.bind("<<ComboboxSelected>>", lambda e: self.update_preview())
        
        # Initial preview update
        self.update_preview()
        
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password.configure(show="")
        else:
            self.password.configure(show="*")
            
    def update_preview(self):
        prefix = self.email_prefix.get()
        number = self.email_number.get()
        domain = self.email_domain.get()
        preview = format_email(prefix, number, domain)
        self.account_preview.configure(state="normal")
        self.account_preview.delete(0, tk.END)
        self.account_preview.insert(0, preview)
        self.account_preview.configure(state="readonly")
        
    def on_next(self):
        """Handle next button click"""
        self.register_callback(
            base_email=self.email_prefix.get(),
            start_number=self.email_number.get(),
            domain=self.email_domain.get(),
            password=self.password.get(),
            headless=self.headless_var.get()
        )
        
    def update_log(self, message):
        """Update log display with new message"""
        self.log_display.configure(state="normal")
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.see(tk.END)  # 自动滚动到最新内容
        self.log_display.configure(state="disabled")
        self.root.update()  # 强制更新界面
        
    def run(self):
        """Start the GUI event loop"""
        self.root.mainloop()
