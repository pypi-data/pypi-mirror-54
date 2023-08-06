import pymysql
import pandas as pd
from sqlalchemy import create_engine
pymysql.install_as_MySQLdb()
def createconnect(connect):
    conn = pymysql.Connect(
            host    = connect.get('host'),
            port    = connect.get('port'),
            user    = connect.get('user'),
            passwd  = connect.get('passwd'),
            db      = connect.get('db'),
            charset = connect.get('charset')
            )
    return conn

def loaddata(connect,sql):
    '''
    :param connect: 链接数据库信息
    :param sql: sql语句
    :return: 响应数据
    '''
    conn = createconnect(connect)
    data = pd.read_sql(sql, conn)
    conn.close()
    return data

def savedata(connect,data,tablename,if_exists='append',index=False,chunksize=10000):
    engine = create_engine(r'mysql+mysqldb://{user}:{psd}@{host}:{port}/{db}?charset=utf8'.format(
                user = connect.get('user'),
                psd = connect.get('passwd'),
                host = connect.get('host'),
                port = connect.get('port'),
                db = connect.get('db')
            ))
    #pandas 版本号
    pd_version = int(pd.__version__.split('.')[1])
    #根据pandas的版本号传入相应的值
    if pd_version<=18:
        pd.io.sql.to_sql(
            data,
            tablename,
            con=engine,
            flavor='mysql',
            if_exists=if_exists,
            index=index,
            chunksize=chunksize
            )
        '''(数据, '表名', con=连接键, schema='数据库名', if_exists='操作方式') 操作方式有append、fail、replace
        append：如果表存在，则将数据添加到这个表的后面
        fail：如果表存在就不操作
        replace：如果存在表，删了，重建'''
    else:
        pd.io.sql.to_sql(
            data,
            tablename,
            con=engine,
            if_exists=if_exists,
            index=index,
            chunksize=chunksize
            )
if __name__ == '__main__':
    print(pd.__version__.split('.')[1])






