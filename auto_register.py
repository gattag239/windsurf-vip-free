"""
Automated registration module for the Windsurf account registration program
"""
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)
from config import (
    REGISTER_URL,
    PROFILE_URL,
    CHROME_EXECUTABLE,
    CHROME_DRIVER,
    CHROME_USER_DATA_DIR,
    CHROME_TEMP_DIR,
    PAGE_LOAD_TIMEOUT,
    ELEMENT_WAIT_TIMEOUT,
    RETRY_INTERVAL,
    ONBOARDING_NAME_URL,
    ONBOARDING_ABOUT_URL,
    ONBOARDING_SOURCE_URL,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    open_chrome_download,
    open_chromedriver_download,
    get_chrome_path,
    get_project_chromedriver_path
)
from utils import show_message, clean_all_chrome_data, check_chrome_versions
import ctypes

class RegistrationBot:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.wait = None
        try:
            clean_all_chrome_data()  # 移除参数
        except Exception as e:
            logging.error(f"Error during cleanup: {e}")
        
    def setup_driver(self):
        """Setup Chrome driver with custom options"""
        try:
            # 检查 Chrome 是否存在
            chrome_path = get_chrome_path()
            if not chrome_path:
                logging.error("未找到Chrome浏览器")
                show_message("错误", "未找到Chrome浏览器。即将打开Chrome下载页面，请安装后重试。")
                open_chrome_download()
                return False

            # 检查 ChromeDriver 是否存在
            chromedriver_path = get_project_chromedriver_path()
            if not chromedriver_path:
                logging.error("未找到ChromeDriver")
                show_message("错误", "未找到ChromeDriver。即将打开ChromeDriver下载页面，请下载对应版本后放入chrome目录。")
                open_chromedriver_download()
                return False

            # Clean all Chrome data
            clean_all_chrome_data()
            
            # Setup Chrome options
            options = webdriver.ChromeOptions()
            options.binary_location = chrome_path
            
            # 基本设置
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # 禁用GPU相关功能
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--disable-gpu-sandbox')
            options.add_argument('--disable-extensions')
            
            # 禁用日志和错误报告
            options.add_argument('--disable-logging')
            options.add_argument('--log-level=3')  # 只显示致命错误
            options.add_argument('--silent')
            
            # 设置用户数据目录
            options.add_argument(f'--user-data-dir={CHROME_USER_DATA_DIR}')
            options.add_argument(f'--disk-cache-dir={CHROME_TEMP_DIR}')
            
            # 创建Chrome服务
            service = Service(executable_path=chromedriver_path)
            
            # 创建Chrome驱动
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            self.wait = WebDriverWait(self.driver, ELEMENT_WAIT_TIMEOUT)
            
            # 设置窗口位置和大小
            screen_width = ctypes.windll.user32.GetSystemMetrics(0)
            x_position = int(screen_width * 0.25)  # 改为屏幕宽度的25%位置
            self.driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
            self.driver.set_window_position(x_position, 50)  # 上边距保持50
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            logging.error(f"设置Chrome驱动时出错: {error_msg}")
            
            if "chromedriver" in error_msg.lower():
                show_message("错误", "ChromeDriver版本可能与Chrome不匹配。即将打开ChromeDriver下载页面，请下载对应版本。")
                open_chromedriver_download()
            elif "chrome" in error_msg.lower():
                show_message("错误", "Chrome浏览器可能未正确安装。即将打开Chrome下载页面。")
                open_chrome_download()
            else:
                show_message("错误", f"设置Chrome驱动时出错: {error_msg}")
            
            if hasattr(self, 'driver') and self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            return False
            
    def cleanup(self):
        """Clean up resources"""
        try:
            if self.driver:
                logging.info("正在清理Chrome进程...")
                try:
                    # 关闭所有标签页
                    self.driver.quit()
                except Exception as e:
                    logging.error(f"关闭Chrome失败: {e}")
                finally:
                    self.driver = None
                    self.wait = None
                
            # 清理Chrome数据
            clean_all_chrome_data()
            logging.info("Chrome数据清理完成")
            
        except Exception as e:
            logging.error(f"Cleanup error: {e}")
            
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.cleanup()
        
    def check_url_status(self):
        """Check current page status"""
        try:
            current_url = self.driver.current_url
            
            # 检查是否在个人资料页面
            if PROFILE_URL in current_url:
                logging.info("检测到已登录账号")
                # 找到并点击退出按钮
                try:
                    logout_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.border-gray-800.text-gray-300"))
                    )
                    self.driver.execute_script("arguments[0].click();", logout_button)
                    logging.info("已点击退出按钮")
                    time.sleep(5)  # 等待5秒
                    return "EMAIL_EXISTS"  # 返回邮箱已存在状态，主程序会自动增加序号
                except Exception as e:
                    logging.error(f"点击退出按钮失败: {e}")
                    return False
            
            # 检查注册页面是否正常显示
            try:
                # 等待页面加载完成
                self.wait.until(
                    EC.presence_of_element_located((By.NAME, "email"))
                )
                logging.info("注册页面加载成功")
                return True
            except TimeoutException:
                # 页面加载出错
                if show_message(
                    "网络错误",
                    "网址无法打开，是否重试？",
                    type_="yesno"
                ):
                    logging.info("用户选择重试")
                    self.driver.refresh()
                    return self.check_url_status()
                logging.info("用户选择不重试，返回主界面")
                return False
            
        except Exception as e:
            logging.error(f"检查页面状态时出错: {e}")
            return False
            
    def handle_onboarding(self):
        """Handle onboarding pages after registration"""
        try:
            # 等待页面完全加载
            self.wait.until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
            
            current_url = self.driver.current_url
            logging.info(f"当前页面URL: {current_url}")
            
            # 处理姓名页面
            if "onboarding?page=name" in current_url:
                logging.info("正在填写姓名信息...")
                try:
                    # 等待姓名输入框出现
                    first_name_input = self.wait.until(
                        EC.presence_of_element_located((By.NAME, "firstName"))
                    )
                    first_name_input.send_keys("John")
                    time.sleep(0.2)  # 减少等待时间
                    
                    last_name_input = self.driver.find_element(By.NAME, "lastName")
                    last_name_input.send_keys("Doe")
                    time.sleep(0.2)  # 减少等待时间
                    
                    # 点击继续按钮
                    continue_button = self.driver.find_element(By.CSS_SELECTOR, "button.bg-brand-dark")
                    self.driver.execute_script("arguments[0].click();", continue_button)
                    
                    # 等待页面变化
                    try:
                        self.wait.until(
                            lambda driver: driver.current_url != current_url
                        )
                        logging.info("已离开姓名页面")
                        return self.handle_onboarding()
                    except TimeoutException:
                        logging.error("等待页面跳转超时")
                        return False
                        
                except Exception as e:
                    logging.error(f"填写姓名时出错: {e}")
                    return False
            
            # 处理任何需要skip的页面（about-user, skills, source等）
            elif any(x in current_url for x in ["onboarding?page=about-user", "onboarding?page=skills", "onboarding?page=source", "/onboarding/source"]):
                page_name = "source" if "source" in current_url else "about-user" if "about-user" in current_url else "skills"
                logging.info(f"正在处理{page_name}页面...")
                try:
                    # 点击跳过按钮 - 使用更精确的选择器
                    skip_button = self.wait.until(
                        EC.presence_of_element_located((
                            By.CSS_SELECTOR, 
                            "button.border-brand-light.text-brand-light"
                        ))
                    )
                    self.driver.execute_script("arguments[0].click();", skip_button)
                    time.sleep(0.2)  # 减少等待时间
                    
                    # 等待页面变化
                    try:
                        # 等待页面完全加载
                        self.wait.until(
                            lambda driver: driver.execute_script('return document.readyState') == 'complete'
                        )
                        
                        # 等待URL变化
                        self.wait.until(
                            lambda driver: driver.current_url != current_url
                        )
                        
                        logging.info(f"已离开{page_name}页面，当前URL: {self.driver.current_url}")
                        
                        # 如果还在onboarding流程中，继续处理
                        if "onboarding" in self.driver.current_url:
                            return self.handle_onboarding()
                        else:
                            logging.info("注册流程完成")
                            return True
                            
                    except TimeoutException:
                        logging.error("等待页面跳转超时")
                        return False
                        
                except Exception as e:
                    logging.error(f"处理{page_name}页面时出错: {e}")
                    return False
            
            else:
                logging.error(f"未知的 onboarding 页面: {current_url}")
                return False
                
        except Exception as e:
            logging.error(f"处理 onboarding 时出错: {e}")
            return False
            
    def register(self, email, password):
        """Perform registration process"""
        try:
            # 只在第一次调用时设置driver
            if not self.driver:
                if not self.setup_driver():
                    show_message("错误", "Chrome浏览器启动失败", type_="error")
                    return False
                    
                # 第一次打开注册页面
                logging.info("正在打开注册页面...")
                self.driver.get(REGISTER_URL)
            else:
                # 如果已经有driver，检查当前页面
                if REGISTER_URL not in self.driver.current_url:
                    logging.info("重新打开注册页面...")
                    self.driver.get(REGISTER_URL)
            
            # 等待页面和表单加载完成
            try:
                logging.info("等待页面加载...")
                # 等待页面完全加载
                self.wait.until(
                    lambda driver: driver.execute_script('return document.readyState') == 'complete'
                )
                
                # 等待表单和邮箱输入框出现
                logging.info("等待表单加载...")
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "form"))
                )
                self.wait.until(
                    EC.presence_of_element_located((By.NAME, "email"))
                )
            except Exception as e:
                logging.error(f"等待页面加载完成时出错: {e}")
                return False
            
            # Fill registration form
            logging.info("正在填写注册信息...")
            
            try:
                # Email
                email_input = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "email"))
                )
                email_input.clear()
                email_input.send_keys(email)
                time.sleep(0.5)
                
                # Password
                password_input = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                password_input.clear()
                password_input.send_keys(password)
                time.sleep(0.5)
                
                # Confirm password
                confirm_input = self.wait.until(
                    EC.presence_of_element_located((By.NAME, "confirmPassword"))
                )
                confirm_input.clear()
                confirm_input.send_keys(password)
                time.sleep(0.5)
                
                # Accept terms
                terms_checkbox = self.wait.until(
                    EC.presence_of_element_located((By.ID, "termsAccepted"))
                )
                if not terms_checkbox.is_selected():
                    self.driver.execute_script("arguments[0].click();", terms_checkbox)
                    time.sleep(0.5)
                
                # Submit form
                logging.info("正在提交注册信息...")
                signup_button = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "button.bg-brand-dark"))
                )
                self.driver.execute_script("arguments[0].click();", signup_button)
                
                # 等待页面变化
                try:
                    # 等待页面完全加载
                    self.wait.until(
                        lambda driver: driver.execute_script('return document.readyState') == 'complete'
                    )
                    
                    # 等待任意一个目标状态出现
                    target_conditions = [
                        lambda driver: "onboarding" in driver.current_url,  # 成功注册
                        lambda driver: PROFILE_URL in driver.current_url,   # 已登录
                        lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "div.text-red-500")) > 0  # 错误消息
                    ]
                    
                    # 持续检查直到满足任一条件
                    max_retries = 60  # 最多等待60次
                    retry_count = 0
                    while retry_count < max_retries:
                        for condition in target_conditions:
                            try:
                                if condition(self.driver):
                                    # 找到目标状态，进行相应处理
                                    current_url = self.driver.current_url
                                    logging.info(f"检测到页面状态变化，当前URL: {current_url}")
                                    
                                    # 处理成功注册
                                    if "onboarding" in current_url:
                                        logging.info("检测到已跳转到 onboarding 页面")
                                        # 继续处理onboarding流程，但不影响注册成功的判断
                                        self.handle_onboarding()
                                        show_message(
                                            "注册成功",
                                            f"账号：{email}\n密码：{password}\n请复制保存",
                                            type_="info"
                                        )
                                        # 注册成功时才清理
                                        self.cleanup()
                                        return True
                                    
                                    # 处理已登录状态
                                    if PROFILE_URL in current_url:
                                        logging.info("检测到已跳转到个人资料页面")
                                        logging.warning(f"邮箱 {email} 已登录")
                                        return "EMAIL_EXISTS"
                                    
                                    # 处理错误消息
                                    error_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.text-red-500")
                                    if error_elements:
                                        for error in error_elements:
                                            text = error.get_attribute('textContent') or error.text
                                            logging.info(f"找到错误消息: {text}")
                                            if "already associated with an account" in text:
                                                logging.warning(f"邮箱 {email} 已存在")
                                                return "EMAIL_EXISTS"
                                        logging.error("存在其他错误消息")
                                        self.cleanup()
                                        return False
                            except Exception as e:
                                logging.warning(f"检查条件时出错: {e}")
                                
                        # 检查网络连接
                        try:
                            self.driver.execute_script("return navigator.onLine;")
                        except Exception as e:
                            logging.error("失去网络连接")
                            self.cleanup()
                            return "TIMEOUT"
                            
                        time.sleep(1)
                        retry_count += 1
                        if retry_count % 10 == 0:  # 每10秒输出一次等待信息
                            logging.info(f"正在等待页面响应... ({retry_count}秒)")
                    
                    logging.warning("等待页面响应超时")
                    self.cleanup()
                    return "TIMEOUT"
                    
                except Exception as e:
                    logging.error(f"等待页面响应时出错: {e}")
                    self.cleanup()
                    return False
                    
            except Exception as e:
                logging.error(f"填写注册表单时出错: {e}")
                logging.exception("详细错误信息:")
                self.cleanup()
                return False
            
        except Exception as e:
            logging.error(f"注册过程出现错误: {e}")
            logging.exception("详细错误信息:")
            self.cleanup()
            return False