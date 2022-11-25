import os
import sqlite3

class SQLiteDb():

    """

    simpleSQLite for sqlite3

    简单封装sqlite

    """
    # 单例模式
    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def open(self, db):
        '''
        打开数据库，使用绝对路径，如果只输入路径默认创建tmp.db
        '''
        if os.path.isabs(db):
            if os.path.isdir(db): db = os.path.join(db,'tmp.db')
            if not db.endswith('.db'): db = db + '.db'
            if os.path.exists(db): print("### The db file: %s is exist already, open it."%db)
            else: print("### Create new sqlite db: ", db)

            self.db = db
            self.conn = sqlite3.connect(self.db)
            self.cursor = self.conn.cursor()
        else:
            print("请输入绝对路径。")
            os.exit()

    def close(self):
        """
        关闭数据库
        """
        self.cursor.close()
        self.conn.close()

    def execute_sql(self,sql,value=None):
        '''
        执行单个sql语句，只需要传入sql语句和值便可
        :param sql: 'insert into user(name,password,number,status) values(?,?,?,?)'
                    'delete from user where name=?'
                    'updata user set status=? where name=?'
                    'select * from user where id=%s'
        :param  value:[(123456,123456,123456,123456),(123,123,123,123)]
                value:'123456'
                value:(123,123)
        :return: result=[1,None]
        '''
        try:
            '''增、删、改'''
            if isinstance(value,list) and isinstance(value[0],(list,tuple)):
                self.cursor.executemany(sql,value)
            else:
                '''执行单条语句：字符串、整型、数组'''
                if value:
                    self.cursor.execute(sql, value)
                else:
                    self.cursor.execute(sql)
            count = self.conn.total_changes
            self.conn.commit()

        except Exception as e:
            print(e)
            return False,e

        if count > 0 :
            return True
        else :
            return False

    def query(self,sql,value=None):
        """
        查询语句
        :param  sql：sql语句
        :param  value：参数,可为None
        :return: 查询结果
        """
        if value is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql,value)

        return self.cursor.fetchall()


if __name__ == "__main__":
    """
    测试代码
    """
    db = SQLiteDb()
    db.open('/home/gitpod/tmp.db')

    res = db.execute_sql("create table baojia (id int UNIQUE, date date UNIQUE, price text null);")
    print(res)

    db.execute_sql("insert into baojia (id,date,price) values (?,?,?);",[(1,'2022/11/11','20'),(2,'11/12/2022','30')])

    res = db.query("select * from baojia;")

    print("shuld be 1-20,2-30", res)

    db.execute_sql("insert into baojia (id,date,price) values (?,?,?);",(3,'11/12/2022','40'))

    res = db.query("select * from baojia where id=?;",(3,))

    print("should be 3-40",res)

    db.close()