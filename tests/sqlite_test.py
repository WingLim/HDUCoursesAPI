import unittest
from content import DBSqlite

class TestSqlite(unittest.TestCase):

    def setUp(self):
        db = DBSqlite()
        db.create_table('db_test')

    def test_insertone(self):
        db = DBSqlite()
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
        "location": "第6教研楼中309",
        "academic": "机械工程学院",
        "other": "18010114"}
        self.assertEqual(db.insert_one('db_test', testdata), 'Insert data succeed')

    def tearDown(self):
        db = DBSqlite()
        db.drop_table('db_test')
    
if __name__ == "__main__":
    unittest.main()
