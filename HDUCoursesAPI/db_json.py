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

    def parse_week(self, time_info, start_end: str):
        start, end = start_end.split("-")

        week_pattern = re.compile(r'{[^}]+}')
        data = {
            'start': 0,
            'end': 0,
            'flag': 0
        }
        info = re.search(week_pattern, time_info).group()
        single = re.search('单周', info)
        double = re.search('双周', info)
        if single is not None:
            data['flag'] = 1
        elif double is not None:
            data['flag'] = 2

        data['start'] = int(start)
        data['end'] = int(end)
        return data

    def parse_time(self, time_info: str, location_info: str):
        times = time_info.split(";")
        locations = location_info.split(";")
        result = []
        for i, item in enumerate(times):
            regex = re.compile(r'第(.{0,8})节')
            regex_result = regex.findall(item)
            course_period_list = []
            for one in regex_result:
                course_period_list.extend(one.split(','))
            course_period_num = len(course_period_list)
            course_period_start = int(course_period_list[0])
            course_period_end = int(course_period_list[course_period_num - 1])
            one = {
                'weekday': item[0:2],
                'start': self.dict_week_start[course_period_start].strftime('%H:%M'),
                'end': self.dict_week_end[course_period_end].strftime('%H:%M'),
                'location': locations[i]
            }
            result.append(one)
        return result

    def parse_location(self, location_info: str):
        locations = location_info.split(";")
        res = set(locations)
        return res

    def parse_other(self, other_info: str):
        return other_info.split(",")

    def cook_course_json(self, export_courses: list[dict]):
        result = []
        for one in export_courses:
            info = {}
            t = one['time']
            if len(t) > 5:
                info['week'] = self.parse_week(t, one['start_end'])
                info['time'] = self.parse_time(t, one['location'])
                one['time_info'] = info
            one['location'] = self.parse_location(one['location'])
            one['other'] = self.parse_other(one['other'])
            one.pop("time")
            one.pop("start_end")
            result.append(one)
        return result
