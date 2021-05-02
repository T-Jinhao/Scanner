from peewee import *
from model.BaseModel import BaseModel

class ScanUrlModel(BaseModel):
    # 时间
    timestamp = DateTimeField()
    # 任务名
    taskname = CharField()
    # taskname唯一编号
    tasknameid = CharField()
    # # 捕获的url
    # current_url = CharField()
    # 扫描的url
    url = CharField()
    # 状态码
    status_code = IntegerField()
    # 文本长度
    content_length = CharField()
    # 标题
    title = CharField()