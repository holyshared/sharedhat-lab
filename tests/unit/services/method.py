import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../tests'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src/libs'))

import unit.models 
from services.method import EventSearchNear
from artbeater.webapi.entity import Response
from artbeater.webapi.parser import ResponseParser

class EventSearchNearTest(unittest.TestCase):

    def setUp(self):
        self._method = EventSearchNear()
        self._query = 'key1=value&key2=value'

    def testSave(self):
        parser = ResponseParser()
        result = parser.parse('response.xml');

        response = Response({ 'result': result })

        cacher = EventSearchNear()
        cacher.save(self._query, response.getResult(), expires=3600);

if __name__ == "__main__":
    unittest.main()
