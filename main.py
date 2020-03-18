from HDUCoursesAPI.course_spider import CourseSpider
from HDUCoursesAPI.db_json import DBJson


if __name__ == "__main__":
    spider = CourseSpider()
    result = spider.run()
    filename = 'course' + spider.year + spider.term
    DBJson(result, filename)