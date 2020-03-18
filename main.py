from HDUCoursesAPI.course_spider import CourseSpider
from HDUCoursesAPI.db_json import DBJson
from HDUCoursesAPI.db_sqlite import DBSqlite



if __name__ == "__main__":
    # 爬取数据
    spider = CourseSpider()
    #result = spider.run()
    filename = 'course' + spider.year + spider.term
    # 将数据写到 json
    json = DBJson()
    #json.write(filename, result)
    # 从 json 中读取数据
    data = json.read(filename)
    # 将数据写入到 sqlite 数据库
    db = DBSqlite()
    db.create_table(filename)
    db.insertmany(filename, data)