import requests
import base64
from openai import OpenAI
import yaml

json_global_data = {
    "token": "",
    "student_id": "",
    "tcc_id": ""
}
#
class Get_Token():
    def __init__(self, username, password):
        self.username = str(username)
        self.password = str(password)

    def get_token(self):
        url = "https://v2.api.z-xin.net/auth/login"
        base64_username, base64_password = self.user_pass_base64()

        data = {
            "username": str(base64_username),
            "password": str(base64_password)
        }

        response = requests.post(url, data=data).json()
        code = response['code']
        msg = response["msg"]
        if code == 2000:
            print("登录成功")
            token = response["data"]["token"]
            json_global_data["token"] = token # 全局变量，存储token

            print(f"token: {token}")
        else:
            print("登录失败")
            print(f"错误信息: {msg}")
            return None

        return token


    def get_stu_info(self):
        url = "https://v2.api.z-xin.net/auth/user"
        #token = self.get_token() # 获取token，这里以后要判断是否获取成功，如果获取失败，则直接返回None
        header = {
            "Authorization": f"Bearer {json_global_data['token']}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=header).json()
        code = response['code']
        msg = response["msg"]
        if code == 2000:
            belongTo = response["data"]["belongTo"]
            email = response["data"]["email"]
            nickname = response["data"]["nickname"]
            id = response["data"]["_id"]
            student_id = self.get_student_id(id)
            tcc_id = self.get_tcc_id(id)

            json_global_data["student_id"] = student_id # 全局变量，存储学生id
            json_global_data["tcc_id"] = str(tcc_id) # 全局变量，存储tcc_id


            json_data = {
                "belongTo": belongTo,
                "email": email,
                "nickname": nickname,
                "id": id,
                "student_id": student_id,
                "tcc_id": tcc_id
            }
            print(json_data)
        else:
            print("获取学生信息失败")

            return None
        return json_data

    def user_pass_base64(self):
        # 要编码的数据，通常是二进制格式
        username_to_encode = self.username.encode('utf-8')
        password_to_encode = self.password.encode('utf-8')

        # 使用base64.b64encode()函数进行编码
        encoded_data_username = base64.b64encode(username_to_encode)
        encoded_data_password = base64.b64encode(password_to_encode)

        # 编码后的结果是bytes类型，可以转换为str类型以便打印或存储
        base64_username = encoded_data_username.decode('utf-8')
        base64_password = encoded_data_password.decode('utf-8')

        return base64_username, base64_password

    def get_student_id(self,id):
        hex_id = str(id)
        # 将16进制数转换为整数
        int_number = int(hex_id, 16)

        # 对整数进行加1操作
        int_number += 1

        # 将结果转换回16进制数
        hex_result = hex(int_number).lower()[2:]

        #print(hex_result)  # 输出加1后的16进制数

        return str(hex_result)

    def get_tcc_id(self,id):
        url = "https://v2.api.z-xin.net/stu/course/getJoinedCourse2"
        header = {
            "Authorization": f"Bearer {json_global_data['token']}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=header).json()
        code = response['code']
        msg = response["msg"]
        if code == 2000:
            tcc_id = response['data'][0]['_id']
            json_global_data["tcc_id"] = str(tcc_id) # 全局变量，存储tcc_id

        else:
            print("获取tcc_id失败")
            print(f"错误信息: {msg}")
            return None
        return tcc_id
    def clear_json_global_data(self):
        json_global_data["token"] = ""
        json_global_data["student_id"] = ""
        json_global_data["tcc_id"] = ""

class Get_homework_afterclass(): #拿到所有题目的标题和ID
    def get_homework_total(self):
        url = "https://v2.api.z-xin.net/stu/homework/filter"
        header = {
            "Authorization" : f"Bearer {json_global_data['token']}",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        data = {
            "category" : "课后作业",
            "student_id": json_global_data["student_id"],
            "tcc_id": json_global_data["tcc_id"]
        }
        response = requests.post(url, headers=header,data=data).json()
        #print(response)
        code = response['code']
        msg = response["msg"]
        if code == 2000:
            total = response["data"]

            json_homework_total = {
                "title": [],
                "id" : [],
                "start_time":[],
                "end_time":[],
            }
            for num in total:
                json_homework_total["title"].append(num["title"])
                json_homework_total["id"].append(num["_id"])
                json_homework_total["start_time"].append(num["starttime"])
                json_homework_total["end_time"].append(num["endtime"])


        else:
            print("获取课后作业失败")
            print(f"错误信息: {msg}")
            return None

        return json_homework_total


class Final_homework():
    def judge_homnework_time(self):
        pass
    def get_homework_info(self,homework_id):
        url = f"https://v2.api.z-xin.net/stu/homework/{homework_id}"
        header = {
            "Authorization" : f"Bearer {json_global_data['token']}",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=header).json()

        homework_info_list = [] # 存储所有题目

        questions = response["data"]["questionSets"][0]["questions"] #拿到所有题目
        set_id = response["data"]["questionSets"][0]["_id"]
        #print(set_id)
        for question in questions:
            #print(question)
            groupname = question["groupName"]
            #print(groupname)
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
                answer_choose = str(answer_choose).replace("\\n", " ").replace("<p>", "").replace("</p>", "")
                answer_content = str(answer["content"]).replace("\\n", " ").replace("<p>", "").replace("</p>", "")

                answer = f"{answer_choose}:{answer_content}  "
                json_homework_info["answer"].append(answer)
            homework_info_list.append(json_homework_info)

        return homework_info_list
    def submit_homework(self,json_data):
        url = "https://v2.api.z-xin.net/stu/question/answerForQuestion"
        header = {
            "Authorization" : f"Bearer {json_global_data['token']}",
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        data={
            "homnework_id":json_data["homework_id"],
            "question_id":json_data["question_id"],
            "questionSet_id":json_data["questionSet_id"],
            "stuAnswer": [
                {
                    "mark": json_data["answer"],"iud3i43v8ud":"="
                }
            ]
        }
        response = requests.post(url, headers=header,data=data).json()
        msg = response["msg"]
        code = response["code"]
        if code == 2000:
            print("提交成功")
        else:
            print("提交失败")
            print(f"错误信息: {msg}")
            return None
        return None

class AI_answer_homework():
    def __init__(self):
        with open("config.yml", "r") as file:
            data = yaml.safe_load(file)
        self.api_key = data["Basic_Information"]["api_key"]

    def get_ai_answer(self,json_data):
        #print(json_data)
        # 将answer列表中的元素用空格连接成字符串
        answer_str = ' '.join(json_data['answer'])

        # 将content和answer_str拼接成一个新的字符串
        combined_string = json_data['content'].strip() + ' ' + answer_str.strip()


        try:
            client = OpenAI(
                # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
                api_key=self.api_key, # https://bailian.console.aliyun.com/#/home 申请地址
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            completion = client.chat.completions.create(
                model="qwen-plus",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                messages=[
                    {'role': 'system',
                     'content': '你更擅长中文和解决C++代码问题。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。'},
                    {'role': 'user',
                     'content':  f"{combined_string} 。'下面的问题如果是单选题请直接告诉我是哪个选项A,B,C,D(不要重复选项后面的内容)，如果是判断题请直接告诉我是T还是F"}
                ]
            )
            #print(completion.choices[0].message.content)
        except Exception as e:
            completion = "A"
            print(f"错误信息：{e}")
            print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")

        json_data={
            "homework_id":json_data["homework_id"],
            "question_id":json_data["question_id"],
            "questionSet_id":json_data["questionSet_id"],
            "answer":completion.choices[0].message.content.upper()
        }
        return json_data

    def cout_homework_answer(self,answer_json,id,title):
        print(f"作业[{title}]：id:{id} 题目id：[{answer_json['question_id']}] 答案：[{answer_json['answer']}]")

        pass


if __name__ == '__main__':
    with open("config.yml", "r") as file:
        data = yaml.safe_load(file)
    username = data["Basic_Information"]["username"]
    password = data["Basic_Information"]["password"]

    Get_Token = Get_Token(username, password)
    Get_Token.get_token() # 将获取到的token存储
    Get_Token.get_stu_info() # 存储获取到的学生ID和tcc_id

    Get_homework_afterclass = Get_homework_afterclass() # 实例化获取课后作业类
    Get_homework_afterclass_data = Get_homework_afterclass.get_homework_total() # 获取所有课后作业的标题和ID


    Final_homework = Final_homework()
    ai_answer = AI_answer_homework()


    len = len(Get_homework_afterclass_data["id"])
    for i in range(len):
        Get_homework_afterclass_data_id = Get_homework_afterclass_data["id"][i] # 遍历所有课后作业的ID
        Get_homework_afterclass_data_title = Get_homework_afterclass_data["title"][i] # 遍历所有课后作业的标题


        Final_homework_data = Final_homework.get_homework_info(Get_homework_afterclass_data_id) # 获取每道题目的信息
        for Final_homework_data_info in Final_homework_data: # 遍历每道题目的信息
            answer = ai_answer.get_ai_answer(Final_homework_data_info)
            cout = AI_answer_homework().cout_homework_answer(answer,Final_homework_data_info["question_id"],Get_homework_afterclass_data_title)
