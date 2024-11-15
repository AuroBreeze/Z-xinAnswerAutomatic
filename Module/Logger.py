import logging
import colorlog

class Logger:
    def __init__(self):
        # 创建日志记录器
        self.logger = colorlog.getLogger('root')  # 创建日志记录器
        # 设置日志输出格式,输出INFO级别的日志
        colorlog.basicConfig(level='INFO', format='%(log_color)s[%(asctime)s][%(name)s][%(levelname)s] %(message)s',
                             datefmt='%Y-%m-%d %H:%M:%S', reset=True)  # 设置日志输出级别
    def Message_Log_Info(self, message):
        # 输出INFO级别的日志
        self.logger.info(message)
    def Message_Log_Error(self, message):
        # 输出ERROR级别的日志
        self.logger.error(message)

