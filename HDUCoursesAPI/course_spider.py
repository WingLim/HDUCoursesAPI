from lxml import etree
from functools import reduce
import requests
import threading
import re
import time

class CourseSpider:
    def __init__(self):
        self.course_url = "http://jxgl.hdu.edu.cn/jxrwcx.aspx" 
        self.s = requests.session()
        self.headers = {
            'Referer': self.course_url,
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16'
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
    def refresh_validation(self, response):
        selector = etree.HTML(response.text)
        viewstate = selector.xpath("//*[@id='__VIEWSTATE']/@value")[0]
        eventvalidation = selector.xpath("//*[@id='__EVENTVALIDATION']/@value")[0]
        self.post_data['__VIEWSTATE'] = viewstate
        self.post_data['__EVENTVALIDATION'] = eventvalidation
    
    # 去除最终结果中的重复项
    def remove_duplication(self, result):
        f = lambda x,y:x if y in x else x + [y]
        result = reduce(f, [[], ] + result)
        return result

    # 选择要爬取的年份和学期
    def select_year_term(self, year, term):
        self.post_data['ddlXN'] = year
        self.post_data['ddlXQ'] = term
        r = self.s.post(self.course_url, data=self.post_data, headers=self.headers)
        self.refresh_validation(r)
        self.post_data.pop('Button1')
        return r.content.decode('gb18030')
    
    # 发送 GET 请求
    def get_request(self):
        r = self.s.get(self.course_url, headers=self.headers)
        self.refresh_validation(r)
        return r.content.decode('gb18030')

    # 发送 POST 请求
    def post_request(self):
        r = self.s.post(self.course_url, data=self.post_data, headers=self.headers)
        self.refresh_validation(r)
        return r.content.decode('gb18030')
    
    # 获取完整的时间、地点、合班的信息
    def get_complete_info(self, course):
        if course.attrib == "":
            return course.text
        else:
            return course.attrib['title']

    # 解析一页中的课程信息
    def parse_course(self, content, num):
        selector = etree.HTML(content)
        course_list = selector.xpath("//*[@id='DBGrid']/tr")[1:-1]
        courses = []
        for one in course_list:
            course = {}
            course['status'] = one.xpath("./td[1]/text()")[0]
            course['title'] = one.xpath("./td[2]/text()")[0]
            course['credit'] = one.xpath("./td[3]/text()")[0]
            course['method'] = one.xpath("./td[4]/text()")[0]
            course['property'] = one.xpath("./td[5]/text()")[0]
            course['teacher'] = one.xpath("./td[6]/text()")[0]
            course['class_id'] = one.xpath("./td[7]/text()")[0]
            course['start_end'] = one.xpath("./td[8]/text()")[0]
            course['time'] = self.get_complete_info(one.xpath("./td[9]")[0])
            course['location'] = self.get_complete_info(one.xpath("./td[10]")[0])
            course['academic'] = one.xpath("./td[11]/text()")[0]
            course['other'] = self.get_complete_info(one.xpath("./td[12]")[0])
            courses.append(course)
        self.page_count = num
        # print("parsed page", num)
        return courses
    
    # 解析页码信息
    def parse_pageinfo(self, content):
        selector = etree.HTML(content)
        pagesinfo = []
        page_count = selector.xpath("//*[@id='DBGrid']/tr[16]/td/a/text()")
        page_script = selector.xpath("//*[@id='DBGrid']/tr[16]/td/a/@href")
        page_data = [re.search(r'DBGrid\$ctl18\$ctl\d+', data).group() for data in page_script]
        pagesinfo.extend(list(zip(page_count, page_data)))
        return pagesinfo
    
    def run(self, year, term):
        result = []
        self.start_time = time.time()
        self.status = 'running'
        self.get_request()
        first_request = self.select_year_term(year, term)
        first_page = self.parse_course(first_request, 1)
        result.extend(first_page)
        pagesinfo = self.parse_pageinfo(first_request)
        i = 0
        while i < len(pagesinfo):
            self.post_data['__EVENTTARGET'] = pagesinfo[i][1]
            next_request = self.post_request()
            next_page = self.parse_course(next_request, pagesinfo[i][0])
            result.extend(next_page)
            if i == len(pagesinfo) - 1 and pagesinfo[i][0] == "...":
                pagesinfo.extend(self.parse_pageinfo(next_request))
                i += 2
            else:
                i += 1
        result = self.remove_duplication(result)
        self.status = 'finished'
        self.end_time = time.time()
        print("total cost", self.end_time - self.start_time)
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
    spider.run('2019-2020', '2')