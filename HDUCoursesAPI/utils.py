def db2dict(data):
    result = []
    key = ['status', 'title', 'credit', 'method', 'property', 'teacher', 
    'class_id', 'start_end', 'time', 'local', 'academic', 'other']
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