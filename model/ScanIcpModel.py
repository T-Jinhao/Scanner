from peewee import *
from model.BaseModel import BaseModel

class ScanIcpModel(BaseModel):
    # 时间
    timestamp = DateTimeField()
    # 任务名
    taskname = CharField()
    # 捕获url编号
    current_wid = CharField()
    # 捕获的url
    capture_url = CharField()