import unittest

from hashlib import md5
from models.artbeat import Method

class MethodModelTest(unittest.TestCase):
 
    def testPut(self):
        method = Method()
        method.hashkey = str(md5('lat=1&lng=2'))
        method.put()

    def testFind(self):
        pass

if __name__ == "__main__":
    unittest.main()