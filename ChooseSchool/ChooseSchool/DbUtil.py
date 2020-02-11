import pymssql
from DBUtils.PooledDB import PooledDB

class Database:
    def __init__(self,db):
        self.host=db[0]
        self.port=None
        self.user=db[1]
        self.pwd=db[2]
        self.db=db[3]
        self._CreatePool()
    def _CreatePool(self):
        if not self.db:
            raise NameError+"没有设置数据库信息"
        self.Pool=PooledDB(creator=pymssql,mincached=2, maxcached=5,maxshared=3, maxconnections=6, blocking=True,host=self.host,user=self.user, \
                               password=self.pwd,database=self.db,charset="utf8")
    def _Getconnect(self):
        self.conn=self.Pool.connection()
        cur=self.conn.cursor()
        if not cur:
            raise "数据库连接不上"
        else:
            return cur
    #查询sql
    def ExecQuery(self,sql):
        cur=self._Getconnect()
        cur.execute(sql)
        relist=cur.fetchall()
        cur.close()
        self.conn.close()
        return relist
    #非查询的sql
    def ExecNoQuery(self,sql):
        cur=self._Getconnect()
        cur.execute(sql)
        self.conn.commit()
        cur.close()
        self.conn.close()