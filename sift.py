# coding: utf8
# laputa

import struct
from stardict import Dict


def is_group(word):
    if word.find(' ') != -1:
        return True
    return False

def sift(ofile, words):
    with open(ofile, 'wb') as fo:
        for w in words:
            if not is_group(w[0]):
                fmt = '%ds' % len(w[0])
                data = struct.pack(fmt, w[0])
                data += '\0'
                data += struct.pack('>ii', w[1], w[2])
                fo.write(data)


if __name__ == '__main__':
    import sys
    dic = Dict(sys.argv[1])
    dic.query('laputa')
    sift(sys.argv[2], dic.words)
