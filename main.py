from HDUCoursesAPI.course_spider import CourseSpider
from HDUCoursesAPI.db_json import DBJson
from HDUCoursesAPI.db_sqlite import DBSqlite

class HDUCourses():
    def __init__(self):
      self.result = []
      self.filename = ''
      self.year = '2020-2021'
      self.term = '2'

    # 爬取数据
    def spidercourse(self):
        spider = CourseSpider()
        self.result = spider.run(self.year, self.term)
        self.filename = 'course' + self.year + self.term
    
    # 将数据写到 json
    def write2json(self):
        json = DBJson()
        json.write(self.filename, self.result)

    # 将数据写入到 sqlite 数据库
    def write2sqlite(self):
        db = DBSqlite()
        db.create_table(self.filename)
        db.insertmany(self.filename, self.result)

    def run(self):
        self.spidercourse()
        self.write2json()
        self.write2sqlite()


if __name__ == "__main__":
    hducourse = HDUCourses()
    hducourse.run()
