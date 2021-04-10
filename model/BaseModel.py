import json
from peewee import *
from sql.pgsql import get_connect
from lib.load_config import Config


class BaseModel(Model):

    class Meta:
        config = Config().readConfig()
        connect_info = config.get("Pgsql", "connect_info")
        connect_info = json.loads(connect_info)
        database = get_connect(connect_info)
