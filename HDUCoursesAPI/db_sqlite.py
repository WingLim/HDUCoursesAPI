import sqlite3

class DBSqlite():

    def __init__(self):
        self.dbname = 'courses.db'
    
    # 连接到数据库
    def connect(self):
        conn = sqlite3.connect(self.dbname)
        cu = conn.cursor()
        return conn, cu
    
    # 关闭连接
    def disconnect(self, conn, cu):
        cu.close()
        conn.close()
    
    # 创建表
    def create_table(self, tablename):
        conn, cu = self.connect()
        cu.execute('''CREATE TABLE '{}'
        (   STATUS TEXT,
            TITLE TEXT,
            CREDIT INT,
            METHOD TEXT,
            PROPERTY TEXT,
            TEACHER TEXT,
            CLASS_ID TEXT PRIMARY KEY NOT NULL,
            START_END TEXT,
            TIME TEXT,
            LOCALTEXT,
            ACADEMIC TEXT,
            OTHER TEXT
        );'''.format(tablename))
        conn.commit()
        self.disconnect(conn, cu)
    
    # 删除表
    def drop_table(self, tablename):
        conn, cu = self.connect()
        sql = 'DROP TABLE IF EXISTS ' + tablename
        cu.execute(sql)
        conn.commit()
        self.disconnect(conn, cu)

    # 插入多条数据
    def insertmany(self, tablename, data):
        data_t = []
        for one in data:
            tmp = tuple(one.values())
            data_t.append(tmp)
        conn, cu = self.connect()
        sql = "INSERT INTO '{}' VALUES (?,?,?,?,?,?,?,?,?,?,?,?)".format(tablename)
        cu.executemany(sql, data_t)
        conn.commit()
        self.disconnect(conn, cu)

    
    # 插入一条数据
    def insertone(self, tablename, data):
        conn, cu = self.connect()
        sql = '''INSERT INTO '{}' VALUES (
            '{status}',
            '{title}',
            {credit},
            '{method}',
            '{property}',
            '{teacher}',
            '{class_id}',
            '{start_end}',
            '{time}',
            '{local}',
            '{academic}',
            '{other}'
        );'''.format(tablename, **data)
        exist = self.__isexist(cu, tablename, data['class_id'])
        if not exist:
            cu.execute(sql)
            conn.commit()
        else:
            print('Data exist')
        self.disconnect(conn, cu)
    
    # 判断数据是否存在
    def __isexist(self, cu, tablename, class_id):
        sql = "SELECT * FROM '{}' WHERE CLASS_ID = '{}';".format(tablename, class_id)
        cu.execute(sql)
        r = cu.fetchall()
        if len(r) > 0:
            return True
        else:
            return False

    def fetch(self, rule):
        pass
    
if __name__ == "__main__":
    testdata = {
        "status": "已开",
        "title": "热工基础(甲)",
        "credit": "3.0",
        "method": "学校组织",
        "property": "学科必修",
        "teacher": "陈昌/刘敬彪",
        "class_id": "(2019-2020-2)-A0106720-41439-1",
        "start_end": "01-16",
        "time": "周四第3,4,5节{第1-16周}",
        "local": "第6教研楼中309",
        "academic": "机械工程学院",
        "other": "18010114"}
    db = DBSqlite()
    #db.create_table('test')
    db.insert('test', testdata)
    #exist = db.isexist('test', '(2019-2020-2)-A0106720-41439-1')
    #print(exist)