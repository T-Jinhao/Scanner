from peewee import *
from model.BaseModel import BaseModel

class ScanPhoneModel(BaseModel):
    # 时间
    timestamp = DateTimeField()
    # 任务名
    taskname = CharField()
    # taskname唯一编号
    tasknameid = CharField()
    # 捕获的url
    current_url = CharField()
    # 手机号
    capture_phone = CharField()