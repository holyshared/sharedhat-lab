import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import artbeat.artbeat
import foursquare.foursquare


from google.appengine.ext import webapp

class MainPage(webapp.RequestHandler):

    def get(self):

#        template_values = {
#                           'greetings': greetings,
#                           'url': url,
#                           'url_linktext': url_linktext,
#                           }

        self.response.headers['Content-Type'] = 'text/html'

        path = os.path.join(os.path.dirname(__file__), 'views/index.html')
        self.response.out.write(template.render(path, {}))


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