# coding: utf-8

import os
import utils
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):

    def __assign(self, values):
        values.update(utils.TEMPLATES_FILES)
        return values

    def get(self):

        self.response.headers['Content-Type'] = 'text/html'

        template_file = os.path.join(utils.TEMPLATES_BASEPATH, 'foursquare/index.html')

        self.response.out.write(template.render(template_file, self.__assign({})))


