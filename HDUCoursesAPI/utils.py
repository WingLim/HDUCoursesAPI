from HDUCoursesAPI.timetable import dict_week_start, dict_week_end
import json
import re


def make_json(data):
    need_deserialization = ['time_info', 'week_info', 'location', 'other']
    for one in data:
        for i in need_deserialization:
            one[i] = one[i].replace("'", "\"")
            one[i] = json.loads(one[i])
    return data

def db2dict(data):
    result = []
    key = ['status', 'title', 'credit', 'method', 'property', 'teacher',
           'class_id', 'time_info', 'week_info', 'location', 'academic', 'other']
    for one in data:
        tmp = dict(zip(key, one))
        result.append(tmp)
    return result


def count2dict(data):
    result = {"count": len(data)}
    tmp = []
    for one in data:
        tmp.append(one[0])
    result["data"] = tmp
    return result


def dict2sql(data):
    sql = "WHERE"
    if 'limit' in data.keys():
        data.pop('limit')
    try:
        data.pop(None)
    except KeyError:
        pass
    if len(data.keys()) >= 1:
        for k, v in data.items():
            v = "'%{}%'".format(v)
            print(k, v)
            sql += ' ' + k + ' LIKE ' + v + ' AND'
        return sql[0:-4]
    else:
        return ''


def parse_week(time_info: str, start_end: str) -> dict:
    week_pattern = re.compile(r'{[^}]+}')
    data = {
        'start': 0,
        'end': 0,
        'flag': 0
    }
    if time_info != "" and time_info != "\xa0" and start_end != "" and start_end != "\xa0":
        start, end = start_end.split("-")
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
                'start': dict_week_start[course_period_start].strftime('%H:%M'),
                'end': dict_week_end[course_period_end].strftime('%H:%M'),
                'location': locations[i]
            }
        else:
            one = {}
        result.append(one)
    return result


def parse_location(location_info: str):
    locations = location_info.split(";")
    return list(set(locations))


def parse_other(other_info: str):
    return other_info.split(",")
