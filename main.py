"""
Main entry point for the Windsurf account registration program
"""
import sys
import logging
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
        """Start the registration process"""
        try:
            # 保存参数
            self.base_email = base_email
            self.current_number = int(start_number)
            self.domain = domain
            self.password = password
            
            # 创建注册机器人
            self.bot = RegistrationBot(headless=not headless)  # 反转headless值
            
            # 尝试注册循环
            number = self.current_number
            
            while True:
                # 生成当前邮箱
                email = format_email(self.base_email, number, self.domain)
                logging.info(f"正在尝试注册账号: {email}")
                
                # 尝试注册
                result = self.bot.register(email, self.password)
                
                if result is True:
                    # 注册成功
                    logger.info(f"账号 {email} 注册成功！")
                    break
                elif result == "EMAIL_EXISTS":
                    # 邮箱已存在或已登录，自动增加序号重试
                    logger.info(f"账号 {email} 已存在或已登录，尝试下一个序号")
                    number += 1
                    continue
                else:
                    # 其他注册失败情况
                    if show_message(
                        "注册失败",
                        "是否重试当前账号？",
                        type_="yesno"
                    ):
                        continue
                    else:
                        break
                        
        except Exception as e:
            logger.error(f"Registration process error: {e}")
            show_message("错误", f"注册过程出现错误：{str(e)}", type_="error")
            
        finally:
            if self.bot:
                self.bot.cleanup()

def cleanup():
    try:
        clean_all_chrome_data()  
    except Exception as e:
        logging.error(f"Error during cleanup: {e}")

def main():
    """Main entry point"""
    try:
        # 清理所有Chrome相关数据
        cleanup()
        
        # 创建注册管理器
        manager = RegistrationManager()
        
        # 创建GUI
        gui = RegistrationGUI(register_callback=manager.start_registration)
        
        # 设置完整的日志记录器
        global logger
        logger = setup_logger(gui)
        
        # 运行GUI
        gui.run()
        
    except Exception as e:
        logger.error(f"Program error: {e}")
        show_message("错误", f"程序运行错误：{str(e)}", type_="error")
        sys.exit(1)

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
        input("Press Enter to exit...")
