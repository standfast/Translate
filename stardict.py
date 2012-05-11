import os
import struct
import sys
import gzip


class Dict(object):
    def __init__(self, dictdir):
        self.words = []
        self.count = 0
        self.dic = ''
        self.idx = ''
        self.ifo = ''
        self.dictdir = dictdir
        self.isload = False

    def query(self, word):
        if not self.isload:
            self._load(self.dictdir)
            self.isload = True
        item = self._get_index(word)
        text = self._query(item[1], item[2]) if item else ''
        return text        

    def _load(self, dictdir):
        self.ifo, self.idx, self.dic = parse_dir(dictdir)
        self._parse_ifo()
        self._parse_idx()

    def _parse_ifo(self):
        with open(self.ifo) as fi:
            for line in fi:
                if line.startswith('wordcount'):
                    _, count = line.strip().split('=')
                    self.count = int(count)

    def _parse_idx(self):
        with open(self.idx, 'rb') as fi: 
            data = fi.read()

        begin = 0

        for _ in xrange(self.count):
            pos = data.find('\0', begin, -1)
            fmt = '%ds' % (pos - begin)
            word = struct.unpack_from(fmt, data, begin)[0]

            begin += struct.calcsize(fmt) + 1
            (offset, size) = struct.unpack_from('>ii', data, begin)
            begin += struct.calcsize('>ii')

            item = (word, offset, size)
            self.words.append(item)

    def _get_index(self, word):
        begin, end = 0, self.count - 1

        while begin <= end:
            mid = (begin + end) >> 1
            r = cmp(word, self.words[mid][0].lower())
            if r > 0:
                begin = mid + 1
            elif r < 0:
                end = mid - 1
            else:
                return self.words[mid]

    def _query(self, offset, size):
        fi =  gzip.open(self.dic, 'rb')
        fi.seek(offset, 0)
        text = fi.read(size)
        fi.close()
        return text

class DictLoadError(Exception):
    pass

def parse_dir(dictdir):
    if not os.path.isdir(dictdir):
        raise DictLoadError('%s not exists' % dictdir)

    ifo, idx, dic = None, None, None

    for f in os.listdir(dictdir):
        if f.endswith('.ifo'):
            ifo = os.path.join(dictdir, f)
        elif f.endswith('.idx'):
            idx = os.path.join(dictdir, f)
        elif f.endswith('.dict.dz'):
            dic = os.path.join(dictdir, f)

    if None in [ifo, idx, dic]:
        raise DictLoadError('ifo, idx or dic file not exists')

    return ifo, idx, dic


if __name__ == "__main__":
    dic = Dict(sys.argv[1])
    print dic.query(sys.argv[2])
    print dic.count
