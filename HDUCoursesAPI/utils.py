from HDUCoursesAPI.timetable import dict_course_start, dict_course_end
import json
import re


def make_json(data: list) -> list:
    need_deserialization = ['time_info', 'week_info', 'location', 'other']
    for one in data:
        for i in need_deserialization:
            one[i] = one[i].replace("'", "\"")
            one[i] = one[i].replace("\\xa0", '')
            one[i] = json.loads(one[i])
    return data


# 判断是否为偶数
def is_even(num):
    if num % 2 == 0:
        return True
    return False


def parse_week(time_info: str, start_end: str) -> dict:
    week_pattern = re.compile(r'{[^}]+}')
    data = {
        'start': 0,
        'end': 0,
        'flag': 0
    }
    if time_info != "" and time_info != "\xa0" and start_end != "" and start_end != "\xa0":
        start, end = map(int, start_end.split("-"))
        info = re.search(week_pattern, time_info).group()
        single = re.search('单周', info)
        double = re.search('双周', info)
        if single is not None:
            data['flag'] = 1
            if is_even(start):
                start += 1
            if is_even(end):
                end -= 1
        elif double is not None:
            data['flag'] = 2
            if not is_even(start):
                start += 1
            if not is_even(end):
                end -= 1
        data['start'] = start
        data['end'] = end
    return data


def parse_time(time_info: str, location_info: str) -> list[dict]:
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

        if course_period_num != 0:
            course_period_start = int(course_period_list[0])
            course_period_end = int(course_period_list[course_period_num - 1])
            one = {
                'weekday': item[0:2],
                'start': dict_course_start[course_period_start].strftime('%H:%M'),
                'end': dict_course_end[course_period_end].strftime('%H:%M'),
                'location': locations[i]
            }
        else:
            one = {}
        result.append(one)
    return result


def parse_location(location_info: str) -> list:
    location_info.replace('\\xa0', '')
    locations = location_info.split(";")
    return list(set(locations))


def parse_other(other_info: str) -> list:
    return other_info.split(",")


b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
idx = "0123456789abcdefghijklmnopqrstuvwxyz"


def hex2b64(h: str) -> str:
    b64pad = "="
    ret = ""
    ii = 0
    for i in range(0, len(h) - 2, 3):
        c = int(h[i:i + 3], 16)
        ret += b64map[c >> 6] + b64map[c & 63]
        ii = i
    ii += 3
    if ii + 1 == len(h):
        c = int(h[ii:ii + 1], 16)
        ret += b64map[c << 2]
    elif ii + 2 == len(h):
        c = int(h[ii:ii + 2], 16)
        ret += b64map[c >> 2] + b64map[(c & 3) << 4]
    while (len(ret) & 3) > 0:
        ret += b64pad
    return ret


def b64tohex(s: str) -> str:
    b64pad = "="
    ret = ""
    k = 0
    slop = 0
    for i in range(len(s)):
        if s[i] == b64pad:
            break
        v = b64map.index(s[i])
        if v < 0:
            continue
        if k == 0:
            ret += idx[v >> 2]
            slop = v & 3
            k = 1
        elif k == 1:
            ret += idx[(v >> 4) | (slop << 2)]
            slop = v & 0xf
            k = 2
        elif k == 2:
            ret += idx[slop]
            ret += idx[v >> 2]
            slop = v & 3
            k = 3
        else:
            ret += idx[(slop << 2) | (v >> 4)]
            ret += idx[v & 0xf]
            k = 0
    if k == 1:
        ret += idx[slop << 2]
    return ret

