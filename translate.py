# coding: utf8

import sublime, sublime_plugin


setting = sublime.load_settings('translate.sublime-settings')


class TranslateListener(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        region = view.word(view.sel()[0])
        symbol = view.substr(region).lower()        
        view.set_status('-', u'中')


class TranslateCommand(sublime_plugin.TextCommand):
    def show(self, alist):
        self.view.window().show_quick_panel(alist, self.on_done)

    def on_done(self, arg):
        if arg != -1:
            print 'hello world'
        print arg

    def run(self, edit):
        region = self.view.word(self.view.sel()[0])
        symbol = self.view.substr(region).lower()
        self.show([symbol])
