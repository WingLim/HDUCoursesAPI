from HDUCoursesAPI.timetable import dict_course_start, dict_course_end
import re


def parse_time(time_info: str, weekday: str, location: str) -> list:
    time_list = time_info.split(',')
    weekday = weekday.replace("星期", "周")
    result = []
    for one in time_list:
        one = one[:-1]
        start, end = map(int, one.split("-"))
        time_one = {
            "weekday": weekday,
            "start": dict_course_start[start].strftime('%H:%M'),
            "end": dict_course_end[end].strftime('%H:%M'),
            "location": location
        }
        result.append(time_one)
    return result


def parse_dup_time(time_info: str, weekday: list, location: list) -> list:
    time_list = time_info.split(',')
    result = []
    for i, one in enumerate(time_list):
        one = one[:-1]
        start, end = map(int, one.split("-"))
        time_one = {
            "weekday": weekday[i],
            "start": dict_course_start[start].strftime('%H:%M'),
            "end": dict_course_end[end].strftime('%H:%M'),
            "location": location[i]
        }
        result.append(time_one)
    return result


def parse_week(week_info: str) -> dict:
    flag = 0
    if '单' in week_info:
        flag = 1
    if '双' in week_info:
        flag = 2
    week_info = re.search(r'\d-\d\d?', week_info).group()
    start, end = week_info.split("-")
    result = {
        "start": int(start),
        "end": int(end),
        "flag": int(flag)
    }
    return result


def parse_location(location: str) -> str:
    location_list = location.split(";")
    if len(location_list) >= 2:
        if location_list[0] == location_list[1]:
            return location_list[0]
    return location
