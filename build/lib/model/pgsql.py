from peewee import *


def get_connect(connect_info):
    '''
    获取数据库连接
    :param connect_info: 连接数据库所需信息
    :return: 数据库对象
    '''
    database = PostgresqlDatabase(
        host=connect_info['host'],
        port=connect_info['port'],
        user=connect_info['user'],
        password=connect_info['password'],
        database=connect_info['database']
    )
    return database


def table_exists(model):
    '''
    判断表是否存在
    :param model: 对象模型
    :return: 存在返回True，不存在返回False
    '''
    return model.table_exists()


def create_table(model):
    '''
    创建表
    :param model: 对象模型
    '''
    # 如果表不存在，创建表
    if not table_exists(model):
        model.create_table()


def drop_table(model):
    '''
    删除表
    :param model: 对象模型
    '''
    # 如果表存在，删除表
    if table_exists(model):
        model.drop_table()


def insert(model, data):
    '''
    向表中插入数据
    :param model: 对象模型
    :param data: 要插入的数据，字典类型，key对应字段，value对应值
    '''
    # 如果表不存在，创建表
    create_table(model)
    # print(data)
    # 向表中插入数据
    model.insert_many(data).execute()


def select(model, where={}):
    '''
    查询表
    :param model: 对象模型
    :param where: 查询条件，dict类型。key表示字段，value表示值
    :return: list类型的结果集
    '''
    # 如果表不存在，创建表
    create_table(model)
    # 格式化where参数
    where_param = __format_where(model, where)
    # 查询
    select_result = model.select().where(where_param).execute()
    # 将结果转换为list类型
    result_list = [result.__data__ for result in select_result]
    return result_list


def delete(model, where):
    '''
    删除表内数据
    :param model: 对象模型
    :param where: 查询条件，dict类型。key表示字段，value表示值
    '''
    # 如果表不存在，创建表
    create_table(model)
    # 格式化where参数
    where_param = __format_where(model, where)
    # 删除
    model.delete().where(where_param).execute()


def update(model, field, where):
    '''
    更新表
    :param model: 对象模型
    :param field: 要更新的字段&值，dict类型。key表示字段，value表示值
    :param where: 查询条件，dict类型。key表示字段，value表示值
    '''
    # 如果表不存在，创建表
    create_table(model)
    # 格式化where参数
    where_param = __format_where(model, where)
    # 更新
    model.update(field).where(where_param).execute()


def __format_where(model, where):
    '''
    将where参数从dict转换为peewee可以识别的格式
    :param model: 对象模型
    :param where: 查询条件，dict类型。key表示字段，value表示值
    :return: peewee可以识别的where参数格式
    '''
    where_param = []
    for key, value in where.items():
        where_param .append(getattr(model, key) == value)
    return where_param
