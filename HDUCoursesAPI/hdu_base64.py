class Base64:
    def __init__(self):

        self.b64map = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        self.b64pad = "="

        self.idx = "0123456789abcdefghijklmnopqrstuvwxyz"

    def hex2b64(self, h) -> str:
        ret = ''
        ii = 0
        for i in range(0, len(h) - 2, 3):
            c = int(h[i:i + 3], 16)
            ret += self.b64map[c >> 6] + self.b64map[c & 63]
            ii = i
        ii += 3
        if ii + 1 == len(h):
            c = int(h[ii:ii + 1], 16)
            ret += self.b64map[c << 2]
        elif ii + 2 == len(h):
            c = int(h[ii:ii + 2], 16)
            ret += self.b64map[c >> 2] + self.b64map[(c & 3) << 4]
        while (len(ret) & 3) > 0:
            ret += self.b64pad
        return ret

    def b64tohex(self, s) -> str:
        ret = ''
        k = 0
        slop = 0
        for i in range(len(s)):
            if s[i] == self.b64pad:
                break
            v = self.b64map.index(s[i])
            if v < 0:
                continue
            if k == 0:
                ret += self.idx[v >> 2]
                slop = v & 3
                k = 1
            elif k == 1:
                ret += self.idx[(v >> 4) | (slop << 2)]
                slop = v & 0xf
                k = 2
            elif k == 2:
                ret += self.idx[slop]
                ret += self.idx[v >> 2]
                slop = v & 3
                k = 3
            else:
                ret += self.idx[(slop << 2) | (v >> 4)]
                ret += self.idx[v & 0xf]
                k = 0
        if k == 1:
            ret += self.idx[slop << 2]
        return ret
