from happybase.util import ensure_bytes
from scrapy.utils.project import get_project_settings
import pymongo
from happybase import Connection, Table

#"读取配置文件并建立数据库连接"
settings = get_project_settings()
class Table2(Table):
    def insert(self,  rowkey, item, familydic={}, family="cf", numbers=5):
        '''
        This is a database write method
        :param db: database object
        :param family: Column family
        :param item: data
        :param numbers:
        :return: Number of failures allowed
        '''
        item = dict(list(map(lambda x:(family+ ":" + x[0], x[1]), item.items())))
        #当familydic存在时将转换列族
        for k, v in familydic.items():
            if item.get(k):
                item[v] = item.pop(k)
        with self.batch() as bat:
            for number in range(numbers):
                try:
                    bat.put(rowkey, item)
                    break
                except:
                    pass

    def exist(self,rowkey,number=5):
        for x in range(number):
            try:
                return self.row(rowkey)
            except:
                pass


class Connection2(Connection):
    def table(self, name, use_prefix=True):
        name = ensure_bytes(name)
        if use_prefix:
            name = self._table_name(name)
        return Table2(name, self)

class Connect_Hbase(object):
    Hbase_ip_port = settings.getdict("HBASE_DB")
    if Hbase_ip_port:
        for k, v in Hbase_ip_port.items():
            HOST, PORT, TABLE = v.split(":")
            try:
                print("正在连接Hbase："+HOST+":"+PORT+":"+TABLE)
                locals()[k] = Connection2(host=HOST, port= int(PORT)).table(TABLE)
                print("连接成功")
            except Exception as e:
                print(HOST+PORT+TABLE+"连接失败",e)
                quit()

class Connect_Mongodb(object):
    MONGO_DB = settings.getdict("MONGO_DB")
    if MONGO_DB:
        for k, v in MONGO_DB.items():
            HOST, PORT, DATABASE, TABLE = v.split(":")
            try:
                print("正在连接：MONGO_DB：" + HOST + PORT + TABLE)
                locals()[k] = pymongo.MongoClient(host=HOST, port= int(PORT))[DATABASE][TABLE]
                print("连接成功")
            except:
                print(HOST + PORT + TABLE + "连接失败")













