# coding: utf-8

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../tests'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src/libs'))

import unit.models
from services.decorator import DataSourceCache
from artbeater.webapi.entity import Response
from artbeater.webapi.parser import ResponseParser

class ServiceMock():

    @DataSourceCache(method='event_searchnear', expires=3600)
    def execute(self, values={}):
        values = {
            'result': {
                'events': [
                    {'name': 'place1'},
                    {'name': 'place1'}
                ]
            }
        }
        return Response(values)

class EventSearchNearTest(unittest.TestCase):

    def setUp(self):
        self._mock = ServiceMock()

    def testSave(self):
        values = { 'key1': 'value', 'key1111': 'value' }
        response = self._mock.execute(values=values)
        print response

if __name__ == "__main__":
    unittest.main()
