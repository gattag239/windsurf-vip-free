"""
Main entry point for the Windsurf account registration program
"""
import sys
import logging
from tkinter import messagebox
from gui import RegistrationGUI
from auto_register import RegistrationBot
from utils import format_email, show_message, clean_all_chrome_data
from logger import setup_logger
from config import CHROME_USER_DATA_DIR, CHROME_TEMP_DIR

# 设置一个基本的日志记录器，用于GUI创建之前的日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger()

class RegistrationManager:
    def __init__(self):
        self.current_number = None
        self.base_email = None
        self.domain = None
        self.password = None
        self.bot = None
        
    def start_registration(self, base_email, start_number, domain, password, headless):
        """Start registration process"""
        try:
            # 保存参数
            self.base_email = base_email
            self.current_number = int(start_number)
            self.domain = domain
            self.password = password
            
            # 创建注册机器人
            if not hasattr(self, 'bot') or self.bot is None:
                self.bot = RegistrationBot(headless=not headless)  # 反转headless值
            
            # 获取当前序号
            current_index = self.current_number
            max_retries = 10  # 最大重试次数
            retry_count = 0
            
            while retry_count < max_retries:
                # 生成邮箱
                email = format_email(self.base_email, current_index, self.domain)
                logger.info(f"开始注册账号 {email}")
                
                # 开始注册
                result = self.bot.register(email, self.password)
                
                if result is True:
                    # 注册成功
                    logger.info(f"账号 {email} 注册成功")
                    self.current_number += 1
                    break
                    
                elif result == "EMAIL_EXISTS":
                    # 邮箱已存在，增加序号重试
                    logger.info(f"账号 {email} 已存在，尝试下一个序号")
                    current_index += 1
                    retry_count += 1
                    continue
                    
                elif result == "TIMEOUT":
                    # 超时，询问是否重试当前账号
                    if show_message(
                        "等待超时",
                        "页面响应超时，是否重试当前账号？",
                        type_="yesno"
                    ):
                        logger.info(f"重试账号 {email}")
                        continue
                    else:
                        logger.info("用户取消重试")
                        break
                        
                else:
                    # 其他错误
                    show_message("错误", "注册过程出现错误", type_="error")
                    break
            
            if retry_count >= max_retries:
                show_message("提示", f"已尝试 {max_retries} 个序号都已存在，请更换邮箱前缀", type_="warning")
            
        except Exception as e:
            logger.error(f"注册过程出现错误: {e}")
            show_message("错误", "注册过程出现错误", type_="error")
            
        finally:
            # 更新界面状态
            pass
            
    def cleanup(self):
        try:
            clean_all_chrome_data()  
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

    @classmethod
    def cleanup(cls):
        try:
            clean_all_chrome_data()  
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")

def main():
    """Main entry point"""
    try:
        # 清理旧的Chrome数据
        RegistrationManager.cleanup()
        
        # 创建注册管理器
        manager = RegistrationManager()
        
        # 创建GUI
        gui = RegistrationGUI(register_callback=manager.start_registration)
        
        # 设置完整的日志记录器
        global logger
        logger = setup_logger(gui)  # 直接传入 GUI 实例
        
        # 运行GUI
        gui.run()
        
    except Exception as e:
        logger.error(f"Program error: {e}")
        show_message("错误", f"程序运行错误：{str(e)}", type_="error")
        sys.exit(1)

    finally:
        # 程序退出时清理
        RegistrationManager.cleanup()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(f"{traceback.format_exc()}\n")
        print(f"Error: {str(e)}")
    finally:
        # 确保在程序退出时清理
        try:
            from utils import clean_all_chrome_data
            clean_all_chrome_data()
        except:
            pass
        # 给用户一些时间看到错误信息
        import time
        time.sleep(3)