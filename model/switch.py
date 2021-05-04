from lib.load_config import Config

def getSwitch():
    '''
    获取数据库启动开关
    :return:
    '''
    config = Config().readConfig()
    switch = config.getboolean("Pgsql", "save")
    return switch