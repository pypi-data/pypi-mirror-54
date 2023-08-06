from com.fw.utils.id_util import IDUtils
from com.fw.base.base_exception import BaseException
import inspect

'''
主要是做dao数据库低层封装
1：get set str
2：字段反射
3：常用属性
'''


class BaseDao(object):
    table_name = None
    service_name = None

    def __init__(self, id=None):
        if not id:
            id = IDUtils.get_primary_key()
        self.id = id

    def get_value(self, key):
        return self.__dict__.get(key)

    def set_value(self, key, value):
        self.__dict__[key] = value;

    def __str__(self):
        print(self.__dict__)

    def get_keys(self):
        return self.__dict__.keys()

    def __check_param(self):
        data_dict = self.__dict__

        if not data_dict:
            raise BaseException("THE DAO NO ATTRIBUTES")

        if "id" not in data_dict or not data_dict["id"]:
            raise BaseException("THE DAO PRIMARY KEY IS NONE")

        if len(data_dict) <= 1:
            raise BaseException("THE DAO ATTRIBUTE IS TOO LESS")

    def get_dict_value(self):
        result = self.__dict__.copy()

        if "mongo_dao" in  result.keys():
            result.pop("mongo_dao")
            result.pop("mysql_dao")

        return result

    @staticmethod
    def get_dao_fileds(T):
        data = inspect.signature(T.__init__).parameters
        result = []
        result.append("id")
        for key, val in data.items():
            if key != "self" and key != 'args' and key != 'kwargs' and key != 'mongo_dao' and key != 'mysql_dao':
                result.append(key)
        return result

    @staticmethod
    def dict_to_dao(data: dict):
        dao = BaseDao()
        for key, val in data.items():
            dao.set_value(key, val)
        return dao

    def delete(self, db="mysql", **kwargs):
        from com.fw.db.mongo_db import mongo_dao
        from com.fw.db.mysql_db import mysql_dao

        if not id or id == "":
            raise BaseException("缺少必要参数")
        '''
        删除根据id
        :param id:
        :return:
        '''
        try:
            if db == "mysql":
                mysql_dao.delete_by_id(self.table_name, self.id, **kwargs)
            else:
                mongo_dao.remove_by_id(self.table_name, self.id, **kwargs)
        except Exception as e:
            raise BaseException("删除{}数据失败:".format(self.service_name if self.service_name else self.table_name), e)

    def insert(self, db="mysql", **kwargs):
        from com.fw.db.mongo_db import mongo_dao
        from com.fw.db.mysql_db import mysql_dao
        '''
        插入数据
        :param dao:
        :return:
        '''
        try:
            if db == "mysql":
                mysql_dao.insert(self, **kwargs)
            else:
                mongo_dao.save(self, **kwargs)
        except Exception as e:
            raise BaseException("保存{}失败".format(self.service_name if self.service_name else self.table_name), e)

    def update_dao(self, db="mysql", **kwargs):
        from com.fw.db.mongo_db import mongo_dao
        from com.fw.db.mysql_db import mysql_dao
        '''
        修改数据
        :param dao:
        :return:
        '''

        if self.id == None or self.id == "":
            raise BaseException("缺少必要参数")
        try:
            if db == "mysql":
                mysql_dao.update_dao(self, **kwargs)
            else:
                mongo_dao.save(self, **kwargs)
        except Exception as e:
            raise BaseException("修改{}数据失败".format(self.service_name if self.service_name else self.table_name), e)


