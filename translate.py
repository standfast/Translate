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
maxline = setting.get('maxline', 5)
maxline = maxline if maxline > 0 else 5
history = setting.get('history', False)


class LocalfileTranslateCommand(sublime_plugin.TextCommand):
    def show(self, alist):
        self.view.window().show_quick_panel(alist, self.on_done)

    def on_done(self, arg):
        if arg != -1:
            if arg == maxline:
                res = self.query(self.symbol)
                self.show(res)
            elif arg == maxline + 1:
                pass
        else:
            pass

    def run(self, edit):
        region = self.view.word(self.view.sel()[0])
        self.symbol = self.view.substr(region).lower()
        res = self.query(self.symbol, maxline)
        self.show(res)

    def query(self, word, maxline=None):
        text = dic.query(word)
        res = parse.parse_langdao(text, maxline)
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
