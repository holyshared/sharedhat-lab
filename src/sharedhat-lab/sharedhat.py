import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import artbeat.artbeat
import foursquare.foursquare
import utils

class MainPage(webapp.RequestHandler):

    def __assign(self, values):
        values.update(utils.TEMPLATES_FILES)
        return values

    def get(self):

        self.response.headers['Content-Type'] = 'text/html'

        path = os.path.join(utils.TEMPLATES_BASEPATH, 'index.html')
        self.response.out.write(template.render(path, self.__assign({})))

application = webapp.WSGIApplication([
    ('/', MainPage),
    ('/artbeat', artbeat.artbeat.MainPage),
    ('/foursquare', foursquare.foursquare.MainPage)
    ], debug=True
)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()