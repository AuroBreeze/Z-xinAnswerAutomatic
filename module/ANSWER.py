from module.AI_Answer import AI_answer_homework
from module.Get_Homework_Info import Get_homework_afterclass_single
from module.Logger import Logger
class ANSWER:
    def choose_homework_and_answer(self, Get_homework_afterclass_data):
        Logger().Message_Log_Info("以下是所有课后作业：")
        for i in range(len(Get_homework_afterclass_data["title"])):
            print(f"{i + 1}. {Get_homework_afterclass_data['title'][i]}")

        while True:
            try:
                num = int(input("请输入你要提交的作业的序号："))
                if num <= 0 or num > len(Get_homework_afterclass_data["title"]):
                    Logger().Message_Log_Info("输入的序号超出范围")
                else:
                    break
            except:
                Logger().Message_Log_Error("输入的序号有误")
        Get_homework_afterclass_data_id = Get_homework_afterclass_data["id"][num - 1] # 遍历所有课后作业的ID
        Get_homework_afterclass_data_title = Get_homework_afterclass_data["title"][num - 1] # 遍历所有课后作业的标题

        Final_homework_data = Get_homework_afterclass_single().get_homework_info(Get_homework_afterclass_data_id) # 获取每道题目的信息
        for Final_homework_data_info in Final_homework_data: # 遍历每道题目的信息
            answer = AI_answer_homework().get_ai_answer(Final_homework_data_info)
            cout = AI_answer_homework().cout_homework_answer(answer,Final_homework_data_info["question_id"],Get_homework_afterclass_data_title)
        Logger().Message_Log_Info("获取答案完成")