import pymongo
import re


def handle_filters(filters: dict) -> dict:
    weekday = ''
    if 'weekday' in filters.keys():
        weekday = filters['weekday']
        filters.pop('weekday')

    filters = fuzzy_query(filters)
    if weekday != '':
        filters['time_info'] = {'$elemMatch': {'weekday': weekday}}

    return filters


def fuzzy_query(filters: dict) -> dict:
    for key, value in filters.items():
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
