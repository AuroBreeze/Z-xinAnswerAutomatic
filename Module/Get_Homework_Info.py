import time
import requests

from Module.Shared_Data import json_global_data_stu,json_homework_total_afterclass,json_homework_single_afterclass
from Module.Logger import Logger


class Get_homework_afterclass_total(): #拿到所有题目的标题和ID

    def choose_homework(self):
        while True:
            try:
                print("[-]:请选择你要查找的作业："
                "1）. 课后作业 2）. 课前预习 "
                "3）. 课堂作业 4）. 课程实验 ")

                choose = int(input("[-]:请输入你要查找的作业序号："))
                if choose == 1:
                    homework_type = "课后作业"
                    return homework_type
                elif choose == 2:
                    homework_type = "课前预习"
                    return homework_type
                elif choose == 3:
                    homework_type = "课堂作业"
                    return homework_type
                elif choose == 4:
                    homework_type = "课程实验"
                    return homework_type
                else:
                    print("[-]:输入的序号有误,请重新输入")
            except:
                print("[-]:输入的序号有误")
                homework_type = "课后作业"
                return homework_type



    def get_homework_total(self,homework_type="课后作业"):
        #homework_type = self.choose_homework() #选择要查找的作业类型
        url = "https://v2.api.z-xin.net/stu/homework/filter"
        header = {
            "Authorization" : f"Bearer { json_global_data_stu['token']}",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        data = {
            "category" : f"{homework_type}",
            "student_id":  json_global_data_stu["student_id"],
            "tcc_id":  json_global_data_stu["tcc_id"]
        }
        response = requests.post(url, headers=header,data=data).json()
        #print(response)
        try:
            code = response['code']
            msg = response["msg"]
            if code == 2000:
                total = response["data"]

                for num in total:
                    json_homework_total_afterclass["title"].append(num["title"])
                    json_homework_total_afterclass["id"].append(num["_id"])
                    json_homework_total_afterclass["start_time"].append(num["starttime"])
                    json_homework_total_afterclass["end_time"].append(num["endtime"])

            else:
                print(f"[-]:获取{homework_type}失败")
                print(f"[-]:错误信息: {msg}")

        except:
            print(f"[-]:获取{homework_type}失败")

class Get_homework_afterclass_single(): #拿到每道题目的详情
    def get_homework_info(self, homework_id):
        socres = 0
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

            if groupname == "单选" or groupname == "判断" or groupname == "多选":
                socres += int(question["presetScore"])

            for answer in question["answer"]:
                answer_choose = answer["mark"]
                answer_choose = str(answer_choose).replace("\\n", " ").replace("<p>", " ").replace("</p>", " ")

                answer_content = str(answer["content"]).replace("\\n", " ").replace("<p>", " ").replace("</p>", " ")

                answer = f"{answer_choose}:{answer_content}  "
                json_homework_info["answer"].append(answer)

            homework_info_list.append(json_homework_info)

        return homework_info_list,socres

    def get_homework_info_sorce(self,num):
        url = "https://v2.api.z-xin.net/stu/course/getJoinedCourse2"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.NjZlYWJmYjlmOTJiZDYwMDE4YjY5ODY1.WCvIt246Jgw3g9oBRQEsW5Tu1PvE2_eFWPgOZx-ZsTw",

        }
        response = requests.get(url, headers=headers).json()

        try:
            total_list = response["data"][0]["homework"]
            homework_info = total_list[-num]

            json_homework_single_afterclass["title"] = str(homework_info["title"])
            json_homework_single_afterclass["finalScore"] = str(homework_info["studenthomework"][0]["finalScore"])
            json_homework_single_afterclass["endtime"] = str(homework_info["endtime"])
            json_homework_single_afterclass["correctProgress"] = str(homework_info["studenthomework"][0]["correctProgress"])
            json_homework_single_afterclass["id"] = str(homework_info["_id"])

        except:
            print("[-]:获取作业校准信息失败")


