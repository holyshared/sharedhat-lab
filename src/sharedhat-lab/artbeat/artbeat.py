# coding: utf-8

import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):

    def get(self):

#        template_values = {
#                           'greetings': greetings,
#                           'url': url,
#                           'url_linktext': url_linktext,
#                           }

		self.response.headers['Content-Type'] = 'text/html'

		path = os.path.join(os.path.dirname(__file__), '../views/artbeat/index.html')
		self.response.out.write(template.render(path, {}))
