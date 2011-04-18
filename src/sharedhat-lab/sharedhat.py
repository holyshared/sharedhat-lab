from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import artbeat.artbeat
import foursquare.foursquare

from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, webapp World!')

application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/artbeat', artbeat.artbeat.MainPage),
    ('/foursquare', foursquare.foursquare.MainPage)
    ],
    debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()