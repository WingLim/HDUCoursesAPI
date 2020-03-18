import json

class DBJson():

    def write(self, filename='output', data=None):
        s = json.dumps(data, indent = 4, ensure_ascii=False)
        with open('data/' + filename + '.json', 'w', encoding = 'utf-8') as f:
            f.write(s)

    def read(self, filename='output'):
        with open('data/' + filename + '.json', 'r', encoding='utf8') as f:
            result = json.load(f)
            return result
