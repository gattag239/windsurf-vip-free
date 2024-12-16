"""
Logging module for the Windsurf account registration program
"""
import logging
from logging.handlers import RotatingFileHandler
from config import LOG_FILE, LOG_FORMAT, LOG_DATE_FORMAT

class GUILogHandler(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        
    def emit(self, record):
        msg = self.format(record)
        # 使用GUI类的update_log方法更新日志
        if hasattr(self.text_widget, 'update_log'):
            self.text_widget.update_log(msg)

def setup_logger(text_widget=None):
    """Setup logger with both file and GUI output"""
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatters
    formatter = logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT)
    
    # File handler (with rotation)
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1024*1024,  # 1MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # GUI handler (if text_widget is provided)
    if text_widget is not None:
        gui_handler = GUILogHandler(text_widget)
        gui_handler.setFormatter(formatter)
        logger.addHandler(gui_handler)
    
    return logger
