# coding: utf-8

from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')
