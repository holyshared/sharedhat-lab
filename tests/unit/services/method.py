import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../tests'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src/libs'))

import unit.models
from hashlib import md5
from models.artbeat import Response as ResponseModel
from services.method import EventSearchNear
from artbeater.webapi.entity import Response
from artbeater.webapi.parser import ResponseParser

class EventSearchNearTest(unittest.TestCase):

    def setUp(self):
        rp = ResponseModel.all()
        rp.filter('hashkey = ', md5('Latitude=35.6763&Longitude=139.8105').hexdigest())
        mdl = rp.get()
        if (not mdl == None):
            mdl.delete()

    def testSave(self):
        service = EventSearchNear()
        result1 = service.execute(values={ 'Latitude': 35.6763, 'Longitude': 139.8105 }, expires=3600);
        result2 = service.execute(values={ 'Latitude': 35.6763, 'Longitude': 139.8105 }, expires=3600);

        self.assertEqual(result1, result2)

if __name__ == "__main__":
    unittest.main()
