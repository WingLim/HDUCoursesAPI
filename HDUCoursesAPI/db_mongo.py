import pymongo
import re
from collections import Iterable


def handle_filters(filters: dict) -> dict:
    weekday = ''
    time = ''
    week = ''
    if 'weekday' in filters.keys():
        weekday = filters['weekday']
        filters.pop('weekday')
    if 'time' in filters.keys():
        time = filters['time']
        filters.pop('time')
    if 'week_info' in filters.keys():
        week = filters['week_info']
        filters.pop('week_info')

    filters = fuzzy_query(filters)
    if weekday != '':
        filters['time_info'] = {'$elemMatch': {'weekday': weekday}}
    if time != '':
        start, end = time.split(',')
        if 'time_info' in filters.keys():
            filters['time_info']['$elemMatch'].update({'start': start, 'end': end})
        else:
            filters['time_info'] = {'$elemMatch': {'start': start, 'end': end}}

    if week != '':
        start, end, flag = map(int, week.split(','))
        filters['week_info'] = {'$eq': {'start': start, 'end': end, 'flag': flag}}
    return filters


def fuzzy_query(filters: dict) -> dict:
    for key, value in filters.items():
        if isinstance(value, Iterable):
            tmp_str = '.*'
            for char in value:
                tmp_str += char
                tmp_str += '.*'
            tmp_re = re.compile(tmp_str)
            filters[key] = tmp_re
    return filters


class DBMongo:
    def __init__(self, url, database, tablename):
        self.client = pymongo.MongoClient(url)
        self.courses = self.client[database]
        self.table = self.courses[tablename]

    def find(self, filters: dict, limit: int = 10, page: int = 0):
        new_filters = handle_filters(filters)
        result = []
        skip = 0
        if page != 0:
            skip = page * limit
        for one in self.table.find(new_filters, limit=limit, skip=skip):
            one.pop('_id')
            result.append(one)
        return result

    def insert_many(self, data: list):
        self.table.insert_many(data)
