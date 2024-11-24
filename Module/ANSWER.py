import requests
from Module.AI_Answer import AI_answer_homework
from Module.Get_Homework_Info import Get_homework_afterclass_single
from Module.Shared_Data import json_homework_total_afterclass,json_homework_single_afterclass,json_global_data_stu


class ANSWER:
    def __init__(self):
        self.optparse_choose = ["A","B","C","D",]
        self.optparse_chooses = ["AB","AC","AD","BC","BD","CD","ABC","ABD","ACD","BCD","ABCD"]
        self.optparse_judge = ["T","F"]

    def choose_homework_and_answer(self):
        print("[-]:以下是所有作业：")
        for i in range(len(json_homework_total_afterclass["title"])):
            print(f"[-]:{i + 1}. {json_homework_total_afterclass['title'][i]}")
        while True:
            try:
                index = int(input("[-]:请输入你要提交的作业的序号："))
                json_homework_single_afterclass["index"] = str(index) # 记录用户输入的作业序号,用来获取作业的index以便定位最后的分数

                if index <= 0 or index > len(json_homework_total_afterclass["title"]):
                    print("[-]:输入的序号超出范围")
                else:
                    break
            except:
                print("[-]:输入的序号有误")

        Get_homework_afterclass_data_id = json_homework_total_afterclass["id"][index - 1] # 遍历所有课后作业的ID
        Get_homework_afterclass_data_title = json_homework_total_afterclass["title"][index - 1] # 遍历所有课后作业的标题

        Final_homework_data = Get_homework_afterclass_single().get_homework_info(Get_homework_afterclass_data_id) # 获取每道题目的信息
        scores = Get_homework_afterclass_single().collect_homework_score(Get_homework_afterclass_data_id) # 收集客观题目的分数
        json_homework_single_afterclass["scoreTotal"] = scores # 记录客观题目的总分数

        self.choose_answer_mode(Final_homework_data,Get_homework_afterclass_data_title)
        print("[-]:"+"-"*20)
        print("[-]:获取答案完成")
        self.verify_score()
        print("[-]:" + "-" * 20)

    def choose_answer_mode(self,Final_homework_data,Get_homework_afterclass_data_title):
        homework_answer = []

        print("[-]:请选择答题模式：")
        print("[-]:1. 爆破模式(仅客观题100%正确) 2. AI模式(需要api_key,请在config.json中配置)")
        num = input("[-]:请输入模式序号：")
        if num == "1":
            print("[-]:爆破模式")
            for Final_homework_data_info in Final_homework_data: # 遍历每道题目的信息
                answer =self.blow_up_answer(Final_homework_data_info)
                homework_answer.append(str(answer))

        elif num == "2":
            print("[-]:AI模式")
            for Final_homework_data_info in Final_homework_data:  # 遍历每道题目的信息
                #print(Final_homework_data_info)
                answer = AI_answer_homework().get_ai_answer(Final_homework_data_info)
                cout = AI_answer_homework().cout_homework_answer(answer, Final_homework_data_info["question_id"],
                                                                 Get_homework_afterclass_data_title)

        print(f"[-]:爆破成功,作业:{Final_homework_data_info['homework_id']},答案:{homework_answer}")
    def blow_up_answer(self,Final_homework_data_info):

        scoreTotal = int(json_homework_single_afterclass["scoreTotal"])
        token = json_global_data_stu["token"]
        headers = {
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Authorization" : f"Bearer {token}",
        }
        url = "https://v2.api.z-xin.net/stu/question/answerForQuestion"

        if Final_homework_data_info["groupname"] == "单选":
            for optparse in self.optparse_choose:
                index = int(json_homework_single_afterclass["index"])
                Get_homework_afterclass_single().get_homework_info_sorce(index) # 获取爆破作业的分数

                Score = int(json_homework_single_afterclass["finalScore"])

                answer = [{"mark": choice} for choice in optparse]
                data = {
                    "question_id": f"{Final_homework_data_info['question_id']}",
                    "homework_id": f"{Final_homework_data_info['homework_id']}",
                    "questionSet_id": f"{Final_homework_data_info['questionSet_id']}",
                    "stuAnswer": answer,
                }
                response = requests.post(url, headers=headers, json=data)

                index = int(json_homework_single_afterclass["index"])
                Get_homework_afterclass_single().get_homework_info_sorce(index)
                finalScore = int(json_homework_single_afterclass["finalScore"])
                if finalScore == 0 or finalScore < Score:
                    pass
                elif finalScore > Score or finalScore == scoreTotal:
                    print(f"[-]:爆破成功,作业{Final_homework_data_info['homework_id']},id:{Final_homework_data_info['question_id']},答案:{data['stuAnswer'][0]['mark']},分数:{finalScore}")
                    break
        elif Final_homework_data_info["groupname"] == "判断":
            for optparse in self.optparse_judge:
                index = int(json_homework_single_afterclass["index"])
                Get_homework_afterclass_single().get_homework_info_sorce(index)

                Score = int(json_homework_single_afterclass["finalScore"])

                answer = [{"mark": choice} for choice in optparse]
                data = {
                    "question_id": f"{Final_homework_data_info['question_id']}",
                    "homework_id": f"{Final_homework_data_info['homework_id']}",
                    "questionSet_id": f"{Final_homework_data_info['questionSet_id']}",
                    "stuAnswer": answer,
                }
                response = requests.post(url, headers=headers, json=data)

                index = int(json_homework_single_afterclass["index"])
                Get_homework_afterclass_single().get_homework_info_sorce(index)

                finalScore = int(json_homework_single_afterclass["finalScore"])
                if finalScore == 0 or finalScore < Score:
                    pass
                elif finalScore > Score or finalScore == scoreTotal:
                    #print(f"[-]:爆破失败,答案:{data['stuAnswer'][0]['mark']}")

                    print(f"[-]:爆破成功,作业{Final_homework_data_info['homework_id']},id:{Final_homework_data_info['question_id']},答案:{data['stuAnswer'][0]['mark']},分数:{finalScore}")
                    break
        elif Final_homework_data_info["groupname"] == "多选":
            for optparse in self.optparse_chooses:
                index = int(json_homework_single_afterclass["index"])
                Get_homework_afterclass_single().get_homework_info_sorce(index)

                Score = int(json_homework_single_afterclass["finalScore"])

                answer = [{"mark": choice} for choice in optparse]
                data = {
                    "question_id": f"{Final_homework_data_info['question_id']}",
                    "homework_id": f"{Final_homework_data_info['homework_id']}",
                    "questionSet_id": f"{Final_homework_data_info['questionSet_id']}",
                    "stuAnswer": answer,
                }
                response = requests.post(url, headers=headers, json=data)
                index = int(json_homework_single_afterclass["index"])
                Get_homework_afterclass_single().get_homework_info_sorce(index)

                finalScore = int(json_homework_single_afterclass["finalScore"])
                if finalScore == 0 or finalScore < Score:
                    pass
                else:

                    print(f"[-]:爆破成功,答案:{data['stuAnswer'][0]['mark']}")
        else:
            pass
        return str(data['stuAnswer'][0]['mark'])





    def verify_score(self):
        index = int(json_homework_single_afterclass["index"])
        Get_homework_afterclass_single().get_homework_info_sorce(index)

        scoreTotal = int(json_homework_single_afterclass["scoreTotal"])
        finalScore = int(json_homework_single_afterclass["finalScore"])

        Correctness = (finalScore / scoreTotal)* 100
        print("-"*20)
        print(f"[-]:本次作业的总分数(客观题):{scoreTotal}")
        print(f"[-]:本次作业的答案最终分数:{finalScore}")
        print("-" * 20)
        print(f"本次作业的正确率:{Correctness}%")

    def clear_data(self):
        json_homework_total_afterclass["title"].clear()
        json_homework_total_afterclass["id"].clear()
        json_homework_single_afterclass["start_time"] = ""
        json_homework_single_afterclass["end_time"] = ""






