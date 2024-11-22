import yaml

# Basic_Information:
#   username: ""
#   password: ""
#   api_key: ""
# Job_Information:
#   Interaction_mode: 0 # 0: 自动模式，1: 交互模式
#   Homework: 0 # 0. 课后作业 3. 课程实验 2. 课堂作业 1. 课前预习
#   Examination: 0 # 0. 不使用 1. 期中考试 2. 期末考试
#   Answer_mode: 0 # 0. 自动答题 1. AI答题

class Check_yml:
    def __init__(self):
        with open("config.yml", "r") as ymlfile:
            self.cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
        self.basic_info = self.cfg["Basic_Information"]

        self.username = self.basic_info["username"]
        self.password = self.basic_info["password"]
        self.api_key = self.basic_info["api_key"]

        self.job_info = self.cfg["Job_Information"]
        self.interaction_mode = self.job_info["Interaction_mode"]
        self.homework = self.job_info["Homework"]
        self.examination = self.job_info["Examination"]
        self.answer_mode = self.job_info["Answer_mode"]

    def check_basic_info(self):
        try:
            if self.username == "" or self.password == "":
                return False
            else:
                pass
            if self.api_key == "":
                print("[-]:Warning: api_key is empty.")
                print("[-]:Warning: You may not be able to use the AI answer mode.")
            return True
        except:
            print ("[-]:Error: check basic information failed.")
            return False

    def check_job_info(self):
        try:
            if self.interaction_mode < 0 or self.interaction_mode > 1:
                return False
            if self.homework < 0 or self.homework > 3:
                return False
            if self.examination < 0 or self.examination > 2:
                return False
            if self.answer_mode < 0 or self.answer_mode > 1:
                return False
            return True
        except:
            print ("[-]:Error: check job information failed.")
            return False

    def main(self):
        JFE_1 =self.check_basic_info()
        if JFE_1:
            print("[-]: Check_yml[Basic_Information]: 基本信息填写正确。")
        else:
            print("[-]: Check_yml[Basic_Information]: 基本信息填写有误，请检查填写内容。")
            print("[-]: 正在退出程序...")
            exit()
        JDE_2 =self.check_job_info()
        if JDE_2:
            print("[-]: Check_yml[Job_Information]: 作业信息填写正确。")
        else:
            print("[-]: Check_yml[Job_Information]: 作业信息填写有误，请检查填写内容。")
            print("[-]: 正在退出程序...")
            exit()
        print("[-]: Check_yml: 所有信息填写正确。")