import unittest, sys

from services.method import EventSearchNear

class EventSearchNearTest(unittest.TestCase):

    def setUp(self):
        self._method = EventSearchNear()
 
    def testFindEvent(self):
        values = { 'Latitude': 35.6763, 'Longitude': 139.8105 }
        expires = 1000
        self._method.find(values=values, expires=expires)

if __name__ == "__main__":
    unittest.main()