import os, sys, pickle, unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../tests'))

import unit.models
from hashlib import md5
from datetime import timedelta, datetime
from models.artbeat import Response
from google.appengine.ext import db

class ResponseModelTest(unittest.TestCase):

    def setUp(self):
        self._hashkey = 'lat=1&lng=2'
        rp = Response.all()
        rp.filter('hashkey =', md5(self._hashkey).hexdigest())
        model = rp.get()
        if (not model == None):
            model.delete()

    def testPut(self):
        result = True
        try:
            props = ['hashkey', 'query', 'name', 'cached', 'expired', 'content']
            cached = datetime.now()
            values = {
                'hashkey': md5(self._hashkey).hexdigest(),
                'query': self._hashkey,
                'name': 'testPut',
                'cached': cached,
                'expired': cached + timedelta(seconds=3600),
                'content': pickle.dumps(props)
            }
            rp = Response()
            [setattr(rp, key, values[key]) for key in props]
            rp.put()

            rp = Response.all()
            rp.filter('hashkey =', md5(self._hashkey).hexdigest())
            model = rp.get()
    
            self.assertTrue(isinstance(model, db.Model))
            self.assertTrue(model.name, 'testPut')
        
        except IOError, e:
            result = False


if __name__ == "__main__":
    unittest.main()