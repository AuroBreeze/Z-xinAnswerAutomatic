import yaml
from openai import OpenAI

from module.Logger import Logger

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
                     'content':  f"{combined_string} 。'下面的问题如果是单选题请直接告诉我是哪个选项A,B,C,D(不要重复选项后面的内容)，如果是判断题请直接告诉我是T还是F,如果是填空题请直接告诉第几个空答案是什么，如果是写程序的题请直接将程序写出来(不需要任何解释)。"}
                ]
            )
            #print(completion.choices[0].message.content)
        except Exception as e:
            completion = "A"
            # print(f"错误信息：{e}")
            # print("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
            #
            Logger().Message_Log_Error(f"AI_answer_homework 错误信息：{e}")
            Logger().Message_Log_Error("请参考文档：https://help.aliyun.com/zh/model-studio/developer-reference/error-code")
        json_data={
            "homework_id":json_data["homework_id"],
            "question_id":json_data["question_id"],
            "questionSet_id":json_data["questionSet_id"],
            "answer":completion.choices[0].message.content#.upper()
        }
        return json_data

    def cout_homework_answer(self,answer_json,id,title):
        print(f"作业[{title}]：id:{id} 题目id：[{answer_json['question_id']}] 答案：[{answer_json['answer']}]")
        pass

