from lxml import etree
from HDUCoursesAPI.utils import hex2b64, b64tohex
from HDUCoursesAPI.new_parser import parse_time, parse_week
from course_model import Course
import requests
import time
import jsbn

term_dict = {
    "1": "3",
    "2": "12",
    "3": "16"
}


class NewCourseSpider:
    def __init__(self, userid: str, password: str):
        self.base_url = "http://newjw.hdu.edu.cn/jwglxt"
        self.login_url = self.base_url + "/xtgl/login_slogin.html?time="
        self.s = requests.session()
        self.now_time = str(int(time.time()))
        self.userid = userid
        self.password = password

    def get_index(self) -> requests.Response:
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Referer": self.login_url + self.now_time,
            "Upgrade-Insecure-Requests": "1"
        })
        return self.s.get(self.login_url+self.now_time)

    def get_csrf_token(self) -> str:
        r = self.get_index()
        selector = etree.HTML(r.text)
        token = selector.xpath("//input[@id='csrftoken']/@value")[0]
        return token

    def get_public_key(self) -> tuple[str, str]:
        public_key_url = "/xtgl/login_getPublicKey.html?time="

        r = self.s.get(self.base_url+public_key_url+self.now_time)
        json_result = r.json()
        modulus = b64tohex(json_result['modulus'])
        exponent = b64tohex(json_result['exponent'])
        return modulus, exponent

    def login(self) -> bool:
        token = self.get_csrf_token()
        modulus, exponent = self.get_public_key()

        public_key = jsbn.RSAKey()
        public_key.setPublic(modulus, exponent)
        password = hex2b64(public_key.encrypt(self.password))

        login_data = [
            ("csrftoken", token),
            ("yhm", self.userid),
            ("mm", password),
            ("mm", password),
        ]
        r = self.s.post(self.login_url+self.now_time, data=login_data)
        if r.url.find("login_slogin.html") == -1:
            print("登录成功")
            return True
        else:
            print("登录失败")
            return False

    def get_personal_schedule(self, year: str = "2021", term: str = "1") -> dict:
        if not self.login():
            return {}
        schedule_url = "/kbcx/xskbcx_cxXsKb.html?gnmkdm=N253508&su=" + self.userid
        schedule_index_url = "kbcx/xskbcx_cxXskbcxIndex.html?gnmkdm=N253508&layout=default&su=" + self.userid
        self.s.headers.update({
            "Referer": self.base_url + schedule_index_url
        })

        post_data = [
            ("xnm", year),
            ("xqm", term_dict[term]),
            ("kzlx", "ck")
        ]
        r = self.s.post(self.base_url+schedule_url, data=post_data)
        return r.json()

    def parse_courses(self, raw_courses):
        course_list = raw_courses['kbList']
        courses = []
        for one in course_list:
            course = Course()
            course.title = one['kcmc']
            course.credit = one['xf']
            course.method = one['khfsmc']
            course.property = one['kcxz']
            course.teacher = one['xm']
            course.class_id = one['jxbmc']
            time_info = one['jcor']
            weekday = one['xqjmc']
            course.time_info.append(parse_time(time_info, weekday))
            week_info = one['zcd']
            course.week_info = parse_week(week_info)
            course.location = one['cdmc']
            courses.append(course.__dict__)
        return courses


if __name__ == "__main__":
    import account
    userid = account.userid
    password = account.password
    spider = NewCourseSpider(userid, password)
    spider.get_personal_schedule()
