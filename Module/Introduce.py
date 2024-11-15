import yaml
from Module.Logger import Logger
class Init_Introduce():
    def __init__(self):
        with open('config.yml', 'r') as stream:
            self.config = yaml.load(stream, Loader=yaml.FullLoader)

        self.logger = Logger()
        self.logger.Message_Log_Info("欢迎使用Z-XinAnswerautomatic!")
        self.logger.Message_Log_Info("作者：" + self.config["Software_Information"]['author'])
        self.logger.Message_Log_Info("版本：" + self.config["Software_Information"]['version'])
        self.logger.Message_Log_Info("日期：" + self.config["Software_Information"]['update'])
        self.logger.Message_Log_Info("许可证：" + self.config["Software_Information"]['license'])
        self.logger.Message_Log_Info("GITHUB地址：https://github.com/AuroBreeze/Z-XinAnswerautomatic")
        self.logger.Message_Log_Info("博客地址：" + self.config["Software_Information"]['github'])
        self.logger.Message_Log_Info("此应用仅供学习交流使用，出现其他任何问题，与作者无关。")
        self.logger.Message_Log_Info("请按回车键继续...")
        input()
