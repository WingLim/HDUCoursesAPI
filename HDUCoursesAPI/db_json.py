from datetime import time
import json
import re


class DBJson:
    def __init__(self):
        self.dict_week_start = {
            1: time(8, 5),
            3: time(10, 0),
            6: time(13, 30),
            8: time(15, 15),
            10: time(18, 30),
            11: time(19, 20)
        }
        self.dict_week_end = {
            2: time(9, 40),
            4: time(11, 35),
            5: time(12, 25),
            7: time(15, 5),
            8: time(16, 0),
            9: time(16, 50),
            11: time(20, 5),
            12: time(20, 55)
        }

    def write(self, filename='output', data=None):
        s = json.dumps(data, indent=4, ensure_ascii=False)
        with open('data/' + filename + '.json', 'w', encoding='utf-8') as f:
            f.write(s)

    def read(self, filename='output'):
        with open('data/' + filename + '.json', 'r', encoding='utf8') as f:
            result = json.load(f)
            return result

    def parse_week(self, timeinfo):
        """解析课程每周信息
        Args:
            timeinfo: 课程的时间信息
        Returns:
            一个字典，包含开始周，结束周以及是否单双周
            flag 为 1 则为每周上课，flag 为 2 则为单/双周上课
            例子:
            {
                'start': 1,
                'end': 16,
                'flag': 1
            }
        """
        week_pattern = re.compile(r'{[^}]+}')
        data = {
            'start': 0,
            'end': 0,
            'flag': 0
        }
        info = re.search(week_pattern, timeinfo).group()
        single = re.search('单周', info)
        double = re.search('双周', info)
        if single is not None:
            data['flag'] = 1
        elif double is not None:
            data['flag'] = 2
        dat = re.findall(r'(\d+)', info)
        if dat and len(dat) >= 2:
            data['start'] = int(dat[0])
            data['end'] = int(dat [1])
        return data
    
    def parse_time(self, time_info):
        regex = re.compile(r'第(.{0,8})节')
        result = regex.findall(time_info)
        course_period_list = []
        for one in result:
            course_period_list.extend(one.split(','))
        # 一共几节课
        course_period_num = len(course_period_list)
        # 第一节课是第几节
        course_period_start = int(course_period_list[0])
        # 最后一节是第几节
        course_period_end = int(course_period_list[course_period_num - 1])
        # 开始上课时间
        dtstart_time = self.dict_week_start[course_period_start]
        # 最后一节课下课时间
        dtend_time = self.dict_week_end[course_period_end]
        return dtstart_time, dtend_time
    
    def cook_course_json(self, export_courses):
        result = []
        for one in export_courses:
            info = {}
            t = one['time']
            if len(t) > 5:
                info['week'] = self.parse_week(t)
                info['weekday'] = t[0:2]
                info['start'], info['end'] = (i.strftime('%H:%M') for i in self.parse_time(t)) 
                one['timeinfo'] = info
            result.append(one)
        return result
