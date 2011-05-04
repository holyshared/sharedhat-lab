# coding: utf-8

import modules

class MainPage(modules.ModuleHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.render('artbeat/index.html')
