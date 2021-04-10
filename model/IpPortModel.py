from peewee import *
from model.BaseModel import BaseModel

class IpPortModel(BaseModel):
    # 时间
    timestamp = DateTimeField()
    # 任务名
    taskname = CharField()
    # ip
    ip = CharField()
    # port
    port = IntegerField()
    # banner
    banner = CharField()