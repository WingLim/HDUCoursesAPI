from lxml import etree
from functools import reduce
from HDUCoursesAPI.course_model import Course
from HDUCoursesAPI.utils import parse_week, parse_time, parse_other, parse_location
import requests
import threading
import re
import time


def parse_page_info(content: str) -> list:
    selector = etree.HTML(content)
    pages_info = []
    page_count = selector.xpath("//*[@id='DBGrid']/tr[16]/td/a/text()")
    page_script = selector.xpath("//*[@id='DBGrid']/tr[16]/td/a/@href")
    page_data = [re.search(r'DBGrid\$ctl18\$ctl\d+', data).group() for data in page_script]
    pages_info.extend(list(zip(page_count, page_data)))
    return pages_info


def get_complete_info(course) -> str:
    if course.attrib == "":
        return course.text
    else:
        return course.attrib['title']


def remove_duplication(result: list) -> list:
    f = lambda x, y: x if y in x else x + [y]
    result = reduce(f, [[], ] + result)
    return result


class CourseSpider:
    def __init__(self):
        self.course_url = "http://jxgl.hdu.edu.cn/jxrwcx.aspx"
        self.s = requests.session()
        self.headers = {
            'Referer': self.course_url,
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) '
                          'Chrome/10.0.648.133 Safari/534.16 '
        }
        self.post_data = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__LASTFOCUS': '',
            '__VIEWSTATE': '',
            '__EVENTVALIDATION': '',
            'ddlXY': '',
            'ddlJS': '',
            'kcmc': '',
            'ddlXN': '',
            'ddlXQ': '',
            'DropDownList1': 'kcmc',
            'TextBox1': '',
            'Button1': ' 查 询 '
        }
        self.result_list = []
        self.start_time = 0
        self.end_time = 0
        self.page_count = 0
        self.status = 'ready'

    # 更新 POST 请求中 __VIEWSTATE 和 __EVENTVALIDATION 的值
    def refresh_validation(self, response: requests.Response) -> None:
        selector = etree.HTML(response.text)
        view_state = selector.xpath("//*[@id='__VIEWSTATE']/@value")[0]
        event_validation = selector.xpath("//*[@id='__EVENTVALIDATION']/@value")[0]
        self.post_data['__VIEWSTATE'] = view_state
        self.post_data['__EVENTVALIDATION'] = event_validation

    # 去除最终结果中的重复项

    # 选择要爬取的年份和学期
    def select_year_term(self, year: str, term: str) -> str:
        self.post_data['ddlXN'] = year
        self.post_data['ddlXQ'] = term
        r = self.s.post(self.course_url, data=self.post_data, headers=self.headers)
        self.refresh_validation(r)
        self.post_data.pop('Button1')
        return r.content.decode('gb18030')

    # 发送 GET 请求
    def get_request(self) -> str:
        r = self.s.get(self.course_url, headers=self.headers)
        self.refresh_validation(r)
        return r.content.decode('gb18030')

    # 发送 POST 请求
    def post_request(self) -> str:
        r = self.s.post(self.course_url, data=self.post_data, headers=self.headers)
        self.refresh_validation(r)
        return r.content.decode('gb18030')

    # 解析一页中的课程信息
    def parse_course(self, content: str, num: int) -> list[dict]:
        selector = etree.HTML(content)
        course_list = selector.xpath("//*[@id='DBGrid']/tr")[1:-1]
        courses = []
        for one in course_list:
            course = Course()
            course.status = one.xpath("./td[1]/text()")[0]
            course.title = one.xpath("./td[2]/text()")[0]
            course.credit = float(one.xpath("./td[3]/text()")[0])
            course.method = one.xpath("./td[4]/text()")[0]
            course.property = one.xpath("./td[5]/text()")[0]
            course.teacher = one.xpath("./td[6]/text()")[0]
            course.class_id = one.xpath("./td[7]/text()")[0]
            start_end = one.xpath("./td[8]/text()")[0]
            time_info = get_complete_info(one.xpath("./td[9]")[0])
            location_info = get_complete_info(one.xpath("./td[10]")[0])
            location = parse_location(location_info)
            course.time_info = parse_time(time_info, location_info)
            course.week_info = parse_week(time_info, start_end)
            course.location = location
            course.academic = one.xpath("./td[11]/text()")[0]
            other_info = get_complete_info(one.xpath("./td[12]")[0])
            course.other = str(parse_other(other_info))
            courses.append(course.__dict__)
        self.page_count = num
        print(f"正在解析第 {num} 页...")
        return courses

    def run(self, year: str, term: str) -> list[dict]:
        result = []
        self.start_time = time.time()
        self.status = 'running'
        self.get_request()
        first_request = self.select_year_term(year, term)
        first_page = self.parse_course(first_request, 1)
        result.extend(first_page)
        pages_info = parse_page_info(first_request)
        i = 0
        while i < len(pages_info):
            self.post_data['__EVENTTARGET'] = pages_info[i][1]
            next_request = self.post_request()
            next_page = self.parse_course(next_request, pages_info[i][0])
            result.extend(next_page)
            if i == len(pages_info) - 1 and pages_info[i][0] == "...":
                pages_info.extend(parse_page_info(next_request))
                i += 2
            else:
                i += 1
        result = remove_duplication(result)
        self.status = 'finished'
        self.end_time = time.time()

        diff = self.end_time - self.start_time
        m, s = divmod(diff, 60)
        print(f"总共花费时间: {int(m)}:{int(s)}", )
        print(f"总共爬取 {len(result)} 条课程信息")
        return result


class SpiderThread(threading.Thread):
    def __init__(self, year, term):
        self.result = []
        self.filename = ''
        self.year = year
        self.term = term
        self.spider = CourseSpider()
        super().__init__()

    def run(self):
        self.result = self.spider.run(self.year, self.term)
        self.filename = 'course' + self.year + self.term


if __name__ == "__main__":
    spider = CourseSpider()
    spider.run('2020-2021', '2')
