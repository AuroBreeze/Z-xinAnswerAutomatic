import requests
import yaml
from Module.Shared_Data import json_global_data_stu,json_homework_single_afterclass
import pytz
import datetime

class Get_homework_afterclass_total(): #拿到所有题目的标题和ID
    def __init__(self):
        with open("config.yml", "r", encoding="utf-8") as f:
            self.config = yaml.load(f.read(), Loader=yaml.FullLoader)
        self.Job_Information = self.config["Job_Information"]

        self.Interaction_mode = self.Job_Information["Interaction_mode"]
        self.Homework = self.Job_Information["Homework"]
        self.Examination = self.Job_Information["Examination"]
        self.Answer_mode = self.Job_Information["Answer_mode"]

        self.timezone = pytz.timezone("Asia/Shanghai")  # 设置时区为上海时间

    
    def get_homework_total(self):
        url = "https://v2.api.z-xin.net/stu/course/getJoinedCourse2"
        headers = {
            "Authorization" : f"Bearer { json_global_data_stu['token']}",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers).json() 

        if response.get("code") != 2000:
            print("[-]:获取课程信息失败")
            exit(0)
        return response 
    def choose_homework(self,response):
        data = response.get("data",[])

        if data == []:
            print("[-]:暂无信息")

        i = 0
        for content in data:
            
            course = content.get("course",[]).get('name','无课程信息')
            teacher = content.get('teacher',[]).get('user',[]).get('nickname','无老师信息')
            print(f"[-]:编号：{i} |课程名称: {course} | 老师: {teacher}")
            i+=1

        num = int(input("[-]:请输入编号选择课程: "))
        i=0

        for content in data[num].get("homework",[]):
            category = content.get("category", "无类别信息")
            title = content.get("title", "无标题信息")
            creartedAt = content.get("createdAt", "无创建时间信息")
            endtiem = content.get("endtime", "无结束时间信息")

            if datetime.datetime.strptime(endtiem, "%Y-%m-%dT%H:%M:%S.%fZ").astimezone(self.timezone) < datetime.datetime.now(self.timezone):
                end = "已结束"
            else:
                end = "未结束"

            _id = content.get("_id", "无ID信息") 

            finalScore = content.get("studenthomework", [])
            if finalScore != []:
                finalScore = finalScore[0].get("finalScore", 0)  # 爆破的得分，非固定值
            else:
                finalScore = 0
            
            
            json_homework_single_afterclass["title"] = title
            json_homework_single_afterclass["_id"] = _id
            json_homework_single_afterclass["endtime"] = endtiem
            json_homework_single_afterclass["finalSore"] = finalScore   # 爆破的得分，非固定值

            print(f"[-]:编号：{i} |类别: {category} | 标题: {title} | 截至：{end}| 分数: {finalScore}")
            i+=1

        num_1 = int(input("[-]:请输入编号选择作业: "))
        homwork_id = data[num].get("homework",[])[num_1].get("_id","无ID信息")
        return homwork_id,num,num_1  # 返回选择的作业ID



class Get_homework_afterclass_single(): #拿到每道题目的详情

    def collect_homework_score(self, homework_id):
        """
        返回本次作业的总分数(固定值)

        Args:
            homework_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        socres = 0
        url = f"https://v2.api.z-xin.net/stu/homework/{homework_id}"
        header = {
            "Authorization": f"Bearer {json_global_data_stu['token']}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=header).json()

        # print("获取到的json为："+ str(response))
        questions = response["data"]["questionSets"][0]["questions"]  # 拿到所有题目
        for question in questions:
            groupname = question["groupName"]
            if groupname == "单选" or groupname == "判断" or groupname == "多选":
                socres += int(question["presetScore"])
        return socres 
    def get_homework_info(self, homework_id): #单个题目的详情存入json_homework_single_afterclass中并返回，使用AI要循环调用这个函数
        url = f"https://v2.api.z-xin.net/stu/homework/{homework_id}"
        header = {
            "Authorization": f"Bearer {json_global_data_stu['token']}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=header).json()

        homework_info_list = []  # 存储所有题目

        questions = response["data"]["questionSets"][0]["questions"]  # 拿到所有题目
        set_id = response["data"]["questionSets"][0]["_id"]
        for question in questions:
            groupname = question["groupName"]

            json_homework_info = {
                "homework_id": str(homework_id),
                "question_id": question["question_id"],
                "questionSet_id": str(set_id),
                "groupname": groupname,
                "content": "",
                "answer": []
            }
            content = question["content"]
            json_homework_info["content"] = content

            for answer in question["answer"]:
                answer_choose = answer["mark"]
                answer_choose = str(answer_choose).replace("\\n", " ").replace("<p>", " ").replace("</p>", " ")
                answer_content = str(answer["content"]).replace("\\n", " ").replace("<p>", " ").replace("</p>", " ")

                answer = f"{answer_choose}:{answer_content}  "
                json_homework_info["answer"].append(answer)

            homework_info_list.append(json_homework_info)
        # print(homework_info_list)
        homework_info_list_copy = []
        for content in reversed(homework_info_list):
            homework_info_list_copy.append(content)

        return homework_info_list_copy  # 返回所有题目的信息

    def get_homework_info_sorce(self,num,num_1): #单个题目的详情存入json_homework_single_afterclass中并返回，使用AI要循环调用这个函数，爆破题目答案
        url = "https://v2.api.z-xin.net/stu/course/getJoinedCourse2"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.NjZlYWJmYjlmOTJiZDYwMDE4YjY5ODY1.WCvIt246Jgw3g9oBRQEsW5Tu1PvE2_eFWPgOZx-ZsTw",
        }
        response = requests.get(url, headers=headers).json()

        try:
            total_list = response["data"][num]["homework"]
            homework_info = total_list[num_1]

            json_homework_single_afterclass["title"] = str(homework_info["title"])
            json_homework_single_afterclass["finalScore"] = str(homework_info["studenthomework"][0]["finalScore"]) # 爆破的得分，非固定值
            json_homework_single_afterclass["endtime"] = str(homework_info["endtime"])
            json_homework_single_afterclass["_id"] = str(homework_info["_id"])

        except:
            print("[-]:获取作业校准信息失败")


