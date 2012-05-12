# coding: utf8

import urllib2
import json

user_agent = 'sublime plugin'

def qqdict(word, user_agent=user_agent):
    url = 'http://dict.qq.com/dict?q=%s' % word

    try:
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url, headers=headers)
        opener = urllib2.build_opener()
        resp = opener.open(request)
        data = resp.read()
        opener.close()
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
    res = qqdict(sys.argv[1], 'plugin for sublime text 2')
    for r in res:
        print r
