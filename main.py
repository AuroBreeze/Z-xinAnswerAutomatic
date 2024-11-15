__author__ = 'AuroBreeze'
__version__ = '1.0.0'
__date__ = '2024-11-09'
__license__ = 'MIT'
# BLOG URL: https://blog.aurobreeze.top/

from Module.Introduce import Init_Introduce
from Module.LoginIn import LoginIn
from Module.Get_Homework_Info import Get_homework_afterclass_total,Get_homework_afterclass_single
from Module.Shared_Data import json_global_data_stu,json_homework_single_afterclass,json_homework_total_afterclass
from Module.AI_Answer import AI_answer_homework
from Module.ANSWER import ANSWER

if __name__ == '__main__':
    Init_Introduce() # 实例化欢迎类

    LoginIn = LoginIn()
    LoginIn.Get_Token_Main() # 获取token并存储在全局变量json_global_data中

    total_homework = Get_homework_afterclass_total().get_homework_total() # 获取所有课后作业的标题和ID 并存储在全局变量json_homework_total_afterclass中
    ANSWER().choose_homework_and_answer()


