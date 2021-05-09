from HDUCoursesAPI.utils import dict2sql
import sqlite3


# 关闭连接
def disconnect(conn: sqlite3.Connection, cu: sqlite3.Cursor):
    cu.close()
    conn.close()


class DBSqlite:

    def __init__(self):
        self.dbname = 'data/courses.db'
    
    # 连接到数据库
    def connect(self):
        conn = sqlite3.connect(self.dbname)
        cu = conn.cursor()
        return conn, cu

    # 创建表
    def create_table(self, table_name: str) -> None:
        conn, cu = self.connect()
        cu.execute('''CREATE TABLE IF NOT EXISTS '{}'
        (   STATUS TEXT,
            TITLE TEXT,
            CREDIT INT,
            METHOD TEXT,
            PROPERTY TEXT,
            TEACHER TEXT,
            CLASS_ID TEXT PRIMARY KEY NOT NULL,
            TIME_INFO TEXT,
            WEEK_INFO TEXT,
            LOCATION TEXT,
            ACADEMIC TEXT,
            OTHER TEXT
        );'''.format(table_name))
        conn.commit()
        disconnect(conn, cu)
    
    # 删除表
    def drop_table(self, table_name: str) -> None:
        conn, cu = self.connect()
        sql = 'DROP TABLE IF EXISTS ' + table_name
        cu.execute(sql)
        conn.commit()
        disconnect(conn, cu)

    # 插入多条数据
    def insert_many(self, table_name: str, data: list):
        data_t = []
        for one in data:
            tmp = tuple(one.values())
            data_t.append(tmp)
        conn, cu = self.connect()
        sql = "INSERT OR IGNORE INTO '{}' VALUES (?,?,?,?,?,?,?,?,?,?,?,?)".format(table_name)
        cu.executemany(sql, data_t)
        conn.commit()
        disconnect(conn, cu)

    # 插入一条数据
    def insert_one(self, table_name: str, data: dict):
        conn, cu = self.connect()
        sql = '''INSERT INTO '{}' VALUES (
            '{status}',
            '{title}',
            {credit},
            '{method}',
            '{property}',
            '{teacher}',
            '{class_id}',
            '{time_info}',
            '{week_info}',
            '{location}',
            '{academic}',
            '{other}'
        );'''.format(table_name, **data)
        cu.execute(sql)
        conn.commit()
        disconnect(conn, cu)

    # 获取某一列的多行数据
    def fetch_column(self, table_name: str, column: str, data: str, limit: int = 10) -> list:
        conn, cu = self.connect()
        sql = "SELECT * FROM '{}' WHERE {} like '%{}%';".format(table_name, column, data)
        cu.execute(sql)
        r = cu.fetchmany(limit)
        return r
    
    # 获取某一列不重复总数
    def fetch_count(self, table_name: str, column: str) -> list:
        conn, cu = self.connect()
        sql = "SELECT DISTINCT {} FROM '{}';".format(column, table_name)
        cu.execute(sql)
        r = cu.fetchall()
        return r
    
    # 获取数据
    def fetch(self, table_name: str, filters: dict, column: str = None, data: str = None, limit: int = 10) -> list:
        filters[column] = data
        rule = dict2sql(filters)
        print(rule)
        conn, cu = self.connect()
        sql = "SELECT * FROM '{}' {};".format(table_name, rule)
        cu.execute(sql)
        names = [desc[0].lower() for desc in cu.description]
        r = cu.fetchmany(limit)
        res = []
        for one in r:
            res.append(dict(zip(names, one)))
        return res
