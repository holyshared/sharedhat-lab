import os, sys, pickle, unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../tests'))

import unit.models
from hashlib import md5
from datetime import timedelta, datetime
#from datetime import timedelta, datetime, time, date
#from models.artbeat import Method, Venue, Event, Response
from models.artbeat import Response
from google.appengine.ext import db

"""
def totime(value):
    keys = ['hour', 'minute', 'second']
    values = value.split(':')
    return time(**dict([(keys[i], int(v)) for i, v in enumerate(values)]))
"""

class ResponseModelTest(unittest.TestCase):

    def setUp(self):
        self._hashkey = 'lat=1&lng=2'

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
        except IOError, e:
            result = False

    def testGet(self):
        rp = Response.all()
        rp.filter('hashkey', md5(self._hashkey).hexdigest())
        model = rp.get()

        self.assertTrue(isinstance(model, db.Model))
        self.assertTrue(model.name, 'testPut')




"""
class MethodModelTest(unittest.TestCase):

    def setUp(self):
        self._one = 'lat=1&lng=2'
        self._full = 'lat=5&lng=5'

    def testPut(self):
        result = True
        try:
            hashkey = md5(self._one).hexdigest()
            method = Method()
            method.hashkey = hashkey
            method.put()
        except IOError, e:
            result = False

        self.assertTrue(result)

    def testFullPropertyPut(self):
        result = True

        try:
            props = ['hashkey', 'query', 'name', 'cached', 'expired']
            cached = datetime.now()
            values = {
                'hashkey': md5(self._full).hexdigest(),
                'query': self._full,
                'name': 'testFullPropertyPut',
                'cached': cached,
                'expired': cached + timedelta(seconds=3600)
            }
            method = Method()
            [setattr(method, key, values[key]) for key in props]
            method.put()
        except IOError, e:
            result = False

        self.assertTrue(result)

    def testFetch(self):
        hashkey = md5(self._one).hexdigest()

        method = Method.all()
        method.filter('hashkey =', hashkey)
        model = method.fetch(limit=1)

        self.assertTrue(isinstance(model, list))

    def testGet(self):
        hashkey = md5(self._full).hexdigest()
 
        method = Method.all()
        method.filter('hashkey =', hashkey)
        model = method.get()

        self.assertTrue(model.hashkey, md5(self._full).hexdigest())
        self.assertTrue(model.query, self._full)
        self.assertTrue(isinstance(model, db.Model))


class VenueModelTest(unittest.TestCase):

    def setUp(self):
        self._one = 'myname'

    def testFullPropertyPut(self):

        values = {
            'name': self._one,
            'type': 'type',
            'address': 'address',
            'access': 'access',
            'area': 'area',
            'href': 'http://sharedhat.com',
            'phone': '000-1000-1100',
            'openingHour': totime('12:00:00'),
            'closingHour': totime('13:00:00'),
            'scheduleDetails': 'detail',
            'scheduleNote': 'detail'
        }
        venue = Venue()
        props = venue.fields().keys()

        [setattr(venue, key, values[key]) for key in props]
        venue.put()

    def testFetch(self):
        v = Venue.all()
        model = v.fetch(limit=1)
        self.assertTrue(isinstance(model, list))

    def testGet(self):
        v = Venue.all()
        v.filter('name =', 'myname')
        model = v.get()

        self.assertTrue(model.openingHour, totime('12:00:00'))
        self.assertTrue(model.closingHour, totime('13:00:00'))
        self.assertTrue(isinstance(model, db.Model))



class EventModelTest(unittest.TestCase):

    def setUp(self):
        self._one = 'art'

    def testFullPropertyPut(self):
        method = Method.all().filter('hashkey', md5('lat=1&lng=2').hexdigest()).get()
        venue = Venue.all().filter('name =', 'name').get()

        values = {
            'id': self._one,
            'method': method,
            'venue': venue,
            'name': 'key',
            'href': 'http://sharedhat.com',
            'description': '',
            'media': ['one', 'two', 'three'],
            'image': ['http://example.com/30.png', 'http://example.com/80.png'],
            'karma': 1110.222,
            'price': '10000',
            'position': '13, 36',
            'distance': 1200.00,
            'datum': 'wld',
            'dateStart': date.today(),
            'dateEnd': date.today(),
            'daysBeforeEnd': 100,
            'scheduleNote': 'text',
            'permanentEvent': 100
        }

        event = Event()
        props = event.fields().keys()

        [setattr(event, key, values[key]) for key in props]
        event.put()


    def testFetch(self):
        event = Event.all()
        model = event.fetch(limit=1)
        self.assertTrue(isinstance(model, list))

    def testGet(self):
        event = Event.all()
        event.filter('name =', 'key')
        model = event.get()

        self.assertTrue(model.href, 'http://sharedhat.com')
        self.assertTrue(model.price, '10000')
        self.assertTrue(isinstance(model, db.Model))
"""

if __name__ == "__main__":
    unittest.main()