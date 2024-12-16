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
    WINDOW_HEIGHT
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
            # Clean all Chrome data
            clean_all_chrome_data()
            
            # Setup Chrome options
            options = webdriver.ChromeOptions()
            options.binary_location = CHROME_EXECUTABLE
            
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
            service = Service(executable_path=CHROME_DRIVER)
            
            # 创建Chrome驱动
            self.driver = webdriver.Chrome(service=service, options=options)
            self.driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
            self.wait = WebDriverWait(self.driver, ELEMENT_WAIT_TIMEOUT)
            
            # 设置窗口位置和大小
            screen_width = ctypes.windll.user32.GetSystemMetrics(0)
            x_position = int(screen_width * 0.3)  # 改为屏幕宽度的30%位置
            self.driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)
            self.driver.set_window_position(x_position, 50)  # 上边距保持50
            
            return True
            
        except Exception as e:
            logging.error(f"设置Chrome驱动时出错: {e}")
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
            # 等待页面跳转到onboarding name页面
            self.wait.until(lambda driver: ONBOARDING_NAME_URL in driver.current_url)
            logging.info("正在填写用户名信息...")
            
            # 生成随机姓名
            import random
            first_names = ["John", "Jane", "Mike", "Sarah", "David", "Emma"]
            last_names = ["Smith", "Johnson", "Brown", "Davis", "Wilson"]
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            
            # 填写姓名
            first_name_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "firstName"))
            )
            first_name_input.clear()
            first_name_input.send_keys(first_name)
            
            last_name_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "lastName"))
            )
            last_name_input.clear()
            last_name_input.send_keys(last_name)
            
            # 点击Continue按钮
            time.sleep(1)  # 等待按钮可点击
            continue_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            self.driver.execute_script("arguments[0].click();", continue_button)
            logging.info("已点击Continue按钮")
            
            # 等待页面跳转到about页面
            self.wait.until(lambda driver: ONBOARDING_ABOUT_URL in driver.current_url)
            logging.info("正在处理about页面...")
            
            # 点击Skip按钮 - 使用更精确的CSS选择器
            time.sleep(1)  # 等待页面加载
            skip_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].border-brand-light"))
            )
            logging.info("找到Skip按钮，尝试点击")
            self.driver.execute_script("arguments[0].click();", skip_button)
            logging.info("已点击Skip按钮")
            
            # 等待页面跳转到source页面
            self.wait.until(lambda driver: ONBOARDING_SOURCE_URL in driver.current_url)
            logging.info("正在完成注册流程...")
            
            # 点击最后的Skip按钮
            time.sleep(1)
            final_skip_button = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit'].border-brand-light"))
            )
            self.driver.execute_script("arguments[0].click();", final_skip_button)
            logging.info("已完成注册流程")
            
            # 注册成功后立即清理
            self.cleanup()
            return True
            
        except Exception as e:
            logging.error(f"Onboarding process error: {e}")
            self.cleanup()  # 出错时也进行清理
            return False
            
    def register(self, email, password):
        """Perform registration process"""
        try:
            # Setup driver
            if not self.setup_driver():
                show_message("错误", "Chrome浏览器启动失败", type_="error")
                return False
            
            # Open registration page
            logging.info("正在打开注册页面...")
            self.driver.get(REGISTER_URL)
            
            # Check page status
            status = self.check_url_status()
            if status == "EMAIL_EXISTS":
                return "EMAIL_EXISTS"
            elif not status:
                return False
            
            # Fill registration form
            logging.info("正在填写注册信息...")
            
            # Email
            email_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.clear()
            email_input.send_keys(email)
            
            # Password
            password_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(password)
            
            # Confirm password
            confirm_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "confirmPassword"))
            )
            confirm_input.clear()
            confirm_input.send_keys(password)
            
            # Accept terms
            terms_checkbox = self.wait.until(
                EC.presence_of_element_located((By.ID, "termsAccepted"))
            )
            if not terms_checkbox.is_selected():
                self.driver.execute_script("arguments[0].click();", terms_checkbox)
                
            # Submit form
            logging.info("正在提交注册信息...")
            signup_button = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.bg-brand-dark"))
            )
            self.driver.execute_script("arguments[0].click();", signup_button)
            
            # 检查是否出现邮箱已存在的错误
            try:
                error_message = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'already associated with an account')]"))
                )
                if error_message:
                    logging.warning(f"邮箱 {email} 已存在")
                    return "EMAIL_EXISTS"
            except TimeoutException:
                pass  # 没有错误消息，继续注册流程
            
            # 检查是否跳转到了个人资料页面（说明已登录）
            try:
                if PROFILE_URL in self.driver.current_url:
                    logging.warning(f"邮箱 {email} 已登录")
                    return "EMAIL_EXISTS"
            except:
                pass
            
            # Handle onboarding process
            if self.handle_onboarding():
                show_message(
                    "注册成功",
                    f"账号：{email}\n密码：{password}\n请复制保存",
                    type_="info"
                )
                return True
            else:
                return False
                
        except Exception as e:
            logging.error(f"Registration process error: {e}")
            show_message("错误", f"注册过程出现错误：{str(e)}", type_="error")
            return False
            
        finally:
            self.cleanup()
