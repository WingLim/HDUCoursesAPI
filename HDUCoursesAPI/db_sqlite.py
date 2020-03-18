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
            LOCAL TEXT,
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
        cu.execute(sql)
        conn.commit()
        self.disconnect(conn, cu)

    # 获取一类数据
    def fetchone(self, tablename, colume, data):
        conn, cu = self.connect()
        sql = "SELECT * FROM '{}' WHERE {} like '{}';".format(tablename, colume, data)
        cu.execute(sql)
        r = cu.fetchall()
        return r
    
    def fetchmany(self, tablename, colume, data, limit=10):
        conn, cu = self.connect()
        data += '%'
        sql = "SELECT * FROM '{}' WHERE {} like '{}';".format(tablename, colume, data)
        cu.execute(sql)
        r = cu.fetchmany(limit)
        return r
