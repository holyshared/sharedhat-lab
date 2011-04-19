import os

TEMPLATES_BASEPATH = os.path.join(os.path.dirname(__file__), '../views/')
TEMPLATES_FILES = {
    'layout': TEMPLATES_BASEPATH + 'layouts/layout.html',
    'template': TEMPLATES_BASEPATH + 'layouts/template.html',
    'header': TEMPLATES_BASEPATH + 'layouts/partials/header.html',
    'sidebar': TEMPLATES_BASEPATH + 'layouts/partials/sidebar.html',
    'footer': TEMPLATES_BASEPATH + 'layouts/partials/footer.html'
}
