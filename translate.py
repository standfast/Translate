# coding: utf8
# laputa

import sublime, sublime_plugin
import os
import stardict
import netdict
import parse


setting = sublime.load_settings('translate.sublime-settings')
pkgpath = sublime.packages_path()
dicpath = os.path.join(pkgpath, setting.get('dictdir'))
dic     = stardict.Dict(dicpath)
history = setting.get('history', False)


class LocalfileTranslateCommand(sublime_plugin.TextCommand):
    def show(self, items, count=None):
        if count and len(items) > count:
            items = items[:count]
            items.append('more..')
        self.view.window().show_quick_panel(items, self.on_done)

    def on_done(self, arg):
        if arg != -1:
            if arg == maxline:
                self.show(self.tetc)
            elif arg == maxline + 1:
                pass
        else:
            pass

    def run(self, edit):
        maxline = setting.get('maxline', 4)
        maxline = maxline if maxline > 0 else 4
        region = self.view.word(self.view.sel()[0])
        self.symbol = self.view.substr(region).lower()
        self.tetc = self.query(self.symbol)
        self.show(self.tetc, maxline)

    def query(self, word):
        text = dic.query(word)
        res = parse.parse_langdao(text)
        return res

class NetworkTranslateCommand(LocalfileTranslateCommand):
    def query(self, word, maxline=None):
        return netdict.qqdict(word)

class HistoryTranslateListener(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        region = view.word(view.sel()[0])
        symbol = view.substr(region).lower()
        if history:      
            view.set_status('-', u'[ 中 ]')
