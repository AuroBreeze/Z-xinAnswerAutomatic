json_global_data_stu = { #登录所需要的信息 全局数据 此数据全局共享生命周期覆盖整局程序
    "token": "",
    "student_id": "",
    "tcc_id": ""
}

json_homework_total_afterclass = { #全部课后作业信息 全局数据 收取课后作业等信息，拿取该作业的所有的作业信息
    "title": [],
    "id": [],
}

json_homework_single_afterclass = {  #课后作业信息用于校验AI正确率 全局数据
    "title": "",
    "_id":"",
    "endtime":"",
    "standard": "", #作业的正确率，固定值
    "finalScore": 0, #爆破作业的的分数，非固定值
    "scoreTotal": None, #作业应得总分，固定值
 }

