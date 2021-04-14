from peewee import *
from model.BaseModel import BaseModel

class ScanModel(BaseModel):
    # 时间
    timestamp = DateTimeField()
    # 任务名
    taskname = CharField()
    # 当前工作url
    current_url = CharField()
    # 设置此url编号
    current_wid = CharField()