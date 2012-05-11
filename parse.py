# coding: utf8
# laputa

def parse_langdao(text, maxline=None):
    items = text.split('\n')
    if items[0].startswith('*'):
        items[0] = items[0][1:]
    if maxline and len(items) > maxline:
        items = items[:maxline]
        items.append('more..')
    items = [i.decode('utf8') for i in items]
    return items
