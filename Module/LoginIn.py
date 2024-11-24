import requests
import base64
import yaml

from Module.Shared_Data import json_global_data_stu

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
        try:
            code = response['code']
            msg = response["msg"]
            if code == 2000:
                print("[-]:登录成功")
                token = response["data"]["token"]
                json_global_data_stu["token"] = token  # 全局变量，存储token

                print(f"[-]:token: {token}")
            else:

                print("[-]:登录失败")
                print(f"[-]:错误信息: {msg}")
        except:
            print("[-]:登录失败")

    def get_stu_info(self):
        url = "https://v2.api.z-xin.net/auth/user"
        #token = self.get_token() # 获取token，这里以后要判断是否获取成功，如果获取失败，则直接返回None
        header = {
            "Authorization": f"Bearer {json_global_data_stu['token']}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=header).json()
        try:
            code = response['code']
            msg = response["msg"]
            if code == 2000:
                belongTo = response["data"]["belongTo"]
                email = response["data"]["email"]
                nickname = response["data"]["nickname"]
                id = response["data"]["_id"]
                student_id = self.get_student_id(id)
                tcc_id = self.get_tcc_id(id)

                if tcc_id is None:
                    print("[-]:BUG: tcc_id is None,正在退出......")
                    exit();

                json_global_data_stu["student_id"] = student_id  # 全局变量，存储学生id
                json_global_data_stu["tcc_id"] = str(tcc_id)  # 全局变量，存储tcc_id

                json_data = {
                    "belongTo": belongTo,
                    "email": email,
                    "nickname": nickname,
                    "id": id,
                    "student_id": student_id,
                    "tcc_id": tcc_id
                }
                print(f"[-]:学生信息: {json_data}\n")
            else:
                print("[-]:获取学生信息失败")
        except:
            print("[-]:获取学生信息失败")

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
            "Authorization": f"Bearer {json_global_data_stu['token']}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=header).json()
        try:
            code = response['code']
            msg = response["msg"]
            if code == 2000:
                tcc_id = response['data'][0]['_id']
                json_global_data_stu["tcc_id"] = str(tcc_id)  # 全局变量，存储tcc_id
            else:
                print("[-]:获取tcc_id失败")
                return None
            return tcc_id
        except:
            print("[-]:获取tcc_id失败")
            return None

class LoginIn():
    def Get_Token_Main(self):
        with open('config.yml', 'r', encoding='utf-8') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
        username = config["Basic_Information"]['username']
        password = config["Basic_Information"]['password']

        token = Get_Token(username,password).get_token()
        tcc_id_stu = Get_Token(username,password).get_stu_info()

