# coding: utf8
# laputa

def parse_langdao(text):
    items = text.split('\n')
    if items[0].startswith('*'):
        items[0] = items[0][1:]
    items = [i.decode('utf8') for i in items]
    return items
