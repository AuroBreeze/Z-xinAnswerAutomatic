from module.Logger import Logger
class Init_Introduce():
    def __init__(self):
        self.logger = Logger()
        self.logger.Message_Log_Info("欢迎使用Z-XinAnswerautomatic！")
        self.logger.Message_Log_Info("作者：AuroBreeze")
        self.logger.Message_Log_Info("版本：1.0.0")
        self.logger.Message_Log_Info("日期：2024-11-09")
        self.logger.Message_Log_Info("许可证：MIT")
        self.logger.Message_Log_Info("GITHUB地址：https://github.com/AuroBreeze/Z-XinAnswerautomatic")
        self.logger.Message_Log_Info("博客地址：https://blog.aurobreeze.top/")
        self.logger.Message_Log_Info("此应用仅供学习交流使用，出现其他任何问题，与作者无关。")
        self.logger.Message_Log_Info("请按任意键继续...")
        input()
