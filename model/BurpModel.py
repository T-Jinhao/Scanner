from peewee import *
from model.BaseModel import BaseModel

class BurpModel(BaseModel):
    # 时间
    timestamp = DateTimeField()
    # 状态码
    status_code = IntegerField()
    # 标题
    title = CharField()
    # url
    url = CharField()
    # 文本长度
    content_length = CharField()
