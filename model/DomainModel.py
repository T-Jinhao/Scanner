from peewee import *
from model.BaseModel import BaseModel

class DoaminModel(BaseModel):
    # 时间
    timestamp = DateTimeField()
    # 任务名
    taskname = CharField()
    # 解析类型
    parsing_type = CharField()
    # 指向IP
    ip = CharField()
    # 状态码
    status_code = IntegerField()
    # 标题
    title = CharField()
    # 最终url
    url = CharField()
    # 子域名
    subdomain = CharField()
    # 文本长度
    content_length = CharField()
