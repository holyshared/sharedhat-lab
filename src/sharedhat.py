# coding: utf-8

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'libs'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'models'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'services'))

import modules
from modules import artbeat, foursquare

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(modules.ModuleHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.render('index.html')

application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/artbeat', artbeat.MainPage),
    ('/artbeat/event', artbeat.EventPage),
    ('/foursquare', foursquare.MainPage)
    ], debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()