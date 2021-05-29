import json
from HDUCoursesAPI.utils import make_json


class DBJson:
    @staticmethod
    def write(filename='output', data: list = None) -> None:
        with open('data/' + filename + '.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def read(filename='output') -> list:
        with open('data/' + filename + '.json', 'r', encoding='utf8') as f:
            result = json.load(f)
            return make_json(result)
