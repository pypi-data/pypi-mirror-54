import redis
import pymysql



class PyMysql:
    """
    创建一个可以连接mysql数据库的类,可以非常方便的直接使用.
    """
    def __init__(self,host,user,password,db):
        """Create a communication with mysql while create a instance"""
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        db_config = {
            'host': self.host,
            'port': 3306,
            'user': self.user,
            'password': self.password,
            'db': self.db,
            'charset': 'utf8'
        }
        self.conn = pymysql.Connect(**db_config)
        self.cur = self.conn.cursor()

    def operate(self,sql):
        """Used to accept SQL sentence """
        try:
            self.cur.execute(sql)
            self.message = [i for i in self.cur.fetchall()]
        except Exception as e:
            print('您的sql语句有误,已执行回滚,请重新使用!',str(e))
            self.conn.rollback()
        else:
            self.conn.commit()

    def close_db(self):
        """close the communication"""
        self.cur.close()
        self.conn.close()

    def change_db(self,new_db):
        """change the db"""
        self.new_db = new_db
        db_config = {
            'host': self.host,
            'port': 3306,
            'user': self.user,
            'password': self.password,
            'db': self.new_db,
            'charset': 'utf8'
        }
        self.conn = pymysql.Connect(**db_config)
        self.cur = self.conn.cursor()


class PyRedis:
    """
    创建一个可以连接redis数据库的类,可以非常方便的直接使用.
    """
    def __init__(self,host):
        """the instance of connected redis has a attribute which name is red to operate the database"""
        self.host = host
        db_config = {
            'host': self.host,
            'port': 6379,
            'decode_responses': True
        }
        self.red = redis.StrictRedis(**db_config)
        
    
    
if __name__ == '__main__':
    pass
