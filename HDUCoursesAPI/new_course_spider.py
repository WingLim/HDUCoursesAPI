from lxml import etree
from utils import hex2b64, b64tohex
import requests
import time
import jsbn


class NewCourseSpider:
    def __init__(self, userid: str, password: str):
        self.base_url = "http://newjw.hdu.edu.cn/jwglxt/xtgl"
        self.login_url = self.base_url + "/login_slogin.html?time="
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
        public_key_url = "/login_getPublicKey.html?time="

        r = self.s.get(self.base_url+public_key_url+self.now_time)
        json_result = r.json()
        modulus = b64tohex(json_result['modulus'])
        exponent = b64tohex(json_result['exponent'])
        return modulus, exponent

    def login(self):
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
        self.s.post(self.login_url+self.now_time, data=login_data)


if __name__ == "__main__":
    userid = ""
    passowrd = ""
    spider = NewCourseSpider(userid, passowrd)
    spider.login()
