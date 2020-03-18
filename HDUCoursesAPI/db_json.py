import json

class DBJson():

    def __init__(self, data, filename='output'):
        s = json.dumps(data, indent = 4, ensure_ascii=False)
        with open(filename + '.json', 'w', encoding = 'utf-8') as f:
            f.write(s)
