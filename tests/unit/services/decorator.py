# coding: utf-8

import unittest, sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../tests'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../src/libs'))

import unit.models
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

class EventSearchNearTest(unittest.TestCase):

    def testSave1(self):
        value = random()
        mock = ServiceMock()
        response = mock.execute(values={ 'key1': 'value', 'key2': value })
        print response

    def testSave2(self):
        value = random()
        mock = EventSearchNearMock()
        response = mock.execute(values={ 'key1': 'value', 'key2': value })
        print response


if __name__ == "__main__":
    unittest.main()
