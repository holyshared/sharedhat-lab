from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import modules
from modules import artbeat
from modules import foursquare

class MainPage(modules.ModuleHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.render('index.html')


application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/artbeat', artbeat.MainPage),
    ('/foursquare', foursquare.MainPage)
    ], debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()