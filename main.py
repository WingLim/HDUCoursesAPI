from HDUCoursesAPI.course_spider import CourseSpider
from HDUCoursesAPI.db_json import DBJson
from HDUCoursesAPI.db_mongo import DBMongo
from HDUCoursesAPI.config import mongo_url


class HDUCourses:
    def __init__(self):
        self.result = []
        self.filename = ''
        self.year = '2020-2021'
        self.term = '2'

    # 爬取数据
    def spider_course(self):
        spider = CourseSpider()
        self.result = spider.run(self.year, self.term)
        self.filename = 'course' + self.year + self.term

    # 将数据写到 json
    def write2json(self):
        DBJson.write(self.filename, self.result)

    def write2mongo(self):
        db = DBMongo(mongo_url(), 'courses', self.filename)
        db.insert_many(self.result)

    def run(self):
        self.spider_course()
        self.write2json()
        self.write2mongo()


if __name__ == "__main__":
    hdu_course = HDUCourses()
    hdu_course.run()
