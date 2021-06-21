import re


def parse_time(time_info: str, weekday: str) -> dict:
    start, end = time_info.split("-")
    weekday = weekday.replace("星期", "周")
    result = {
        "weekday": weekday,
        "start": start,
        "end": end
    }
    return result


def parse_week(week_info: str) -> dict:
    flag = 0
    if '单' in week_info:
        flag = 1
    if '双' in week_info:
        flag = 2
    week_info = re.search(r'\d-.\d', week_info).group()
    start, end = week_info.split("-")
    result = {
        "start": start,
        "end": end,
        "flag": flag
    }
    return result