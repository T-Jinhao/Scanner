from peewee import *
from model.pgsql import get_connect
from lib.load_config import Config


class BaseModel(Model):

    class Meta:
        config = Config().readConfig()
        connect_info = {
            'host': config.get("Pgsql", "host"),
            'port': config.get("Pgsql", "port"),
            'user': config.get("Pgsql", "user"),
            'password': config.get("Pgsql", "password"),
            'database': config.get("Pgsql", "database")
        }
        database = get_connect(connect_info)
