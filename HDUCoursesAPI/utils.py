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
