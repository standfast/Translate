# coding: utf8

import urllib
import json

def qqdict(word):
    queryurl = 'http://dict.qq.com/dict?q=%s' % word

    try:
        webin = urllib.urlopen(queryurl) 
        data = webin.read()
        webin.close()
    except:
        return ['network error']

    res   = json.loads(data)
    local = res.get('local', [])
    baike = res.get('baike', [])

    result = []

    if local:
        des = local[0]['des']
        for item in des:
            if item.get('p', None):
                result.append('%s %s' % (item['p'], item['d']))
            else:
                result.append(item['d'])
    elif baike:
        # bkstr = baike[0]['abs']
        result = [u'百科']
    else:
        result = ['not found']

    return result


if __name__ == '__main__':
    import sys
    res = query_qqdict(sys.argv[1])
    for r in res:
        print r
