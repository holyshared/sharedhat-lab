# coding: utf-8

import os, modules
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from artbeater.webapi import ArtBeat

class MainPage(webapp.RequestHandler):

    def __assign(self, values):
        values.update(modules.TEMPLATES_FILES)
        return values

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        artbeat = ArtBeat()

        template_file = os.path.join(modules.TEMPLATES_BASEPATH, 'artbeat/index.html')

        self.response.out.write(template.render(template_file, self.__assign({})))


