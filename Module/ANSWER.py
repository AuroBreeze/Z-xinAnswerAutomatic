import time
from Module.AI_Answer import AI_answer_homework
from Module.Get_Homework_Info import Get_homework_afterclass_single
from Module.Shared_Data import json_homework_total_afterclass,json_homework_single_afterclass
from Module.Logger import Logger
class ANSWER:

    def choose_homework_and_answer(self):
        print("以下是所有作业：")
        for i in range(len(json_homework_total_afterclass["title"])):
            print(f"{i + 1}. {json_homework_total_afterclass['title'][i]}")
        while True:
            try:
                #Logger().Message_Log_Info("请输入你要提交的作业的序号：")
                index = int(input("请输入你要提交的作业的序号："))
                json_homework_single_afterclass["index"] = str(index) # 记录用户输入的作业序号,用来获取作业的index以便定位最后的分数

                if index <= 0 or index > len(json_homework_total_afterclass["title"]):
                    print("输入的序号超出范围")
                else:
                    break
            except:
                print("输入的序号有误")
        Get_homework_afterclass_data_id = json_homework_total_afterclass["id"][index - 1] # 遍历所有课后作业的ID
        Get_homework_afterclass_data_title = json_homework_total_afterclass["title"][index - 1] # 遍历所有课后作业的标题

        Final_homework_data,scores = Get_homework_afterclass_single().get_homework_info(Get_homework_afterclass_data_id) # 获取每道题目的信息
        json_homework_single_afterclass["scoreTotal"] = scores

        for Final_homework_data_info in Final_homework_data: # 遍历每道题目的信息
            answer = AI_answer_homework().get_ai_answer(Final_homework_data_info)
            cout = AI_answer_homework().cout_homework_answer(answer,Final_homework_data_info["question_id"],Get_homework_afterclass_data_title)
        print("获取答案完成")
        print("请自行提交完成，按回车键检查正确率(仅支持课后作业)")
        input()
        self.verify_score()

    def verify_score(self):
        index = int(json_homework_single_afterclass["index"])
        Get_homework_afterclass_single().get_homework_info_sorce(index)

        scoreTotal = int(json_homework_single_afterclass["scoreTotal"])
        finalScore = int(json_homework_single_afterclass["finalScore"])

        Correctness = (finalScore / scoreTotal)* 100

        Logger().Message_Log_Info(f"本次作业的总分数(客观题):{scoreTotal}")
        Logger().Message_Log_Info(f"本次作业的AI答案最终分数:{finalScore}")

        print(f"本次作业的正确率:{Correctness}%")

    def clear_data(self):
        json_homework_total_afterclass["title"].clear()
        json_homework_total_afterclass["id"].clear()
        json_homework_single_afterclass["start_time"] = ""
        json_homework_single_afterclass["end_time"] = ""






