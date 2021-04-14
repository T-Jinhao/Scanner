from peewee import *
from model.BaseModel import BaseModel

class ScanMailModel(BaseModel):
    # 时间
    timestamp = DateTimeField()
    # 任务名
    taskname = CharField()
    # 捕获的url编号
    current_wid = CharField()
    # 邮箱
    capture_mail = CharField()