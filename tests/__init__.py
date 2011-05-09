import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../src/libs'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/models'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../src/services'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'unit'))

os.environ['APPLICATION_ID'] = 'sharedhat-lab'

import unittest
from test import test_support

from unit.models.artbeat import ResponseModelTest
from unit.services.decorator import DataStoreCacheTest
from unit.services.method import EventSearchNearTest

def test_main():
    test_support.run_unittest(
        ResponseModelTest,
        DataStoreCacheTest,
        EventSearchNearTest
    )

if __name__ == "__main__":
    test_main()
