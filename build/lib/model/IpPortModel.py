from peewee import *
from model.BaseModel import BaseModel

class IpPortModel(BaseModel):
    # 时间
    timestamp = DateTimeField()
    # 任务名
    taskname = CharField()
    # taskname唯一编号
    tasknameid = CharField()
    # ip
    ip = CharField()
    # port
    port = IntegerField()
    # banner
    banner = CharField()
    # service
    service = CharField()