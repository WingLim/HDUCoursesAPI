import unittest
import os
from HDUCoursesAPI.db_sqlite import DBSqlite


class TestSqlite(unittest.TestCase):
    db = DBSqlite("courses.db")

    def setUp(self):
        self.db.create_table('db_test')

    def test_insert_one(self):
        test_data = {
            "status": "已开",
            "title": "管理统计方法与应用",
            "credit": "3",
            "method": "学校组织",
            "property": "学科必修",
            "teacher": "梁燕华",
            "class_id": "(2020-2021-2)-A0300850-41415-2",
            "time_info": "[{'weekday': '周一', 'start': '10:00', 'end': '12:25', 'location': '第6教研楼北212'}]",
            "week_info": "{'start': 1, 'end': 16, 'flag': 0}",
            "location": "['第6教研楼北212']",
            "academic": "管理学院",
            "other": "['19031312']"
        }
        self.assertIsNone(self.db.insert_one('db_test', test_data))

    def tearDown(self):
        self.db.drop_table('db_test')
        os.remove("courses.db")


if __name__ == "__main__":
    unittest.main()
