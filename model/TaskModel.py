from peewee import *
from model.BaseModel import BaseModel

class TaskModel(BaseModel):
    # 时间
    timestamp = DateTimeField()
    # 任务名
    taskname = CharField()
    # taskname唯一编号
    tasknameid = CharField()
    # 描述
    description = CharField()
    # 目标
    target = CharField()
    # 行为
    action = CharField()
