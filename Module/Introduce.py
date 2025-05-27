import yaml
from Module.Logger import Logger
class Init_Introduce():
    def __init__(self):
        with open('config.yml', 'r',encoding='utf-8') as stream:
            self.config = yaml.load(stream, Loader=yaml.FullLoader)

        print("[-]:欢迎使用Z-XinAnswerautomatic!")
        print("[-]:作者：" + self.config["Software_Information"]['author'])
        print("[-]:版本：" + self.config["Software_Information"]['version'])
        print("[-]:日期：" + self.config["Software_Information"]['update'])
        print("[-]:许可证：" + self.config["Software_Information"]['license'])
        print("[-]:GITHUB地址：https://github.com/AuroBreeze/Z-XinAnswerautomatic")
        print("[-]:博客地址：" + self.config["Software_Information"]['blog'])
        print("[-]:此应用仅供学习交流使用，出现其他任何问题，与作者无关。")
        print("[-]:请按回车键继续...")
        input("[-]:")
