import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

TEMPLATES_BASEPATH = os.path.join(os.path.dirname(__file__), '../templates/')
TEMPLATES_FILES = {
    'layout': TEMPLATES_BASEPATH + 'layouts/layout.html',
    'template': TEMPLATES_BASEPATH + 'layouts/template.html',
    'header': TEMPLATES_BASEPATH + 'layouts/partials/header.html',
    'sidebar': TEMPLATES_BASEPATH + 'layouts/partials/sidebar.html',
    'footer': TEMPLATES_BASEPATH + 'layouts/partials/footer.html'
}

class ModuleHandler(webapp.RequestHandler):

    __values = {}

    def assign(self, values={}):
        self.__values.update(values)

    def render(self, renderTemplate):
        self.__values.update(TEMPLATES_FILES)
        templateFile = os.path.join(TEMPLATES_BASEPATH, renderTemplate)
        self.response.out.write(template.render(templateFile, self.__values))
