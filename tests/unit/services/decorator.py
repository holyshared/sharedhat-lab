# coding: utf-8

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../tests'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src/libs'))

import unit.models
from models.artbeat import Response as ResponseModel
from hashlib import md5
from random import random 
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

class EventSearchNearMock():

    @DataSourceCache(method='event_searchnear', expires=3600)
    def execute(self, values={}):
        parser = ResponseParser()
        res = parser.parse('response.xml')

        return Response({ 'result': res })

class DataStoreCacheTest(unittest.TestCase):

    def setUp(self):
        self._value1 = 100
        self._value2 = 200

        rp = ResponseModel.all()
        rp.filter('hashkey =', md5('key1=value&key2=' + str(self._value1)).hexdigest())
        mdl1 = rp.get()
        if (not mdl1 == None):
            print 'rm1'
            mdl1.delete()

        rp.filter('hashkey =', md5('key1=value&key2=' + str(self._value2)).hexdigest())
        mdl2 = rp.get()
        if (not mdl2 == None):
            print 'rm2'
            mdl2.delete()

    def testSave1(self):
        value = random()
        mock = ServiceMock()
        response1 = mock.execute(values={ 'key1': 'value', 'key2': self._value1 })
        response2 = mock.execute(values={ 'key1': 'value', 'key2': self._value1 })

        self.assertEqual(response1, response2)

    def testSave2(self):
        value = random()
        mock = EventSearchNearMock()
        response1 = mock.execute(values={ 'key1': 'value', 'key2': self._value2 })
        response2 = mock.execute(values={ 'key1': 'value', 'key2': self._value2 })

        self.assertEqual(response1, response2)


if __name__ == "__main__":
    unittest.main()
