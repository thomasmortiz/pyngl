# Set the path for imports
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from uom.unit_converter import UnitConverter
from unittest import TestSuite, TextTestRunner
import settings
import pdb

class TestUnitConverterMethods(unittest.TestCase):
    def setUp(self):
        self.density = 1000.0   # kg/m3
        return
 
    def test_convert_density(self):
        self.assertTrue("cat" == "cat")
        return

   def tearDown(self):
        return
def suite():
    suite = TestSuite()
    suite.addTest(TestUnitConverterMethods('test_convert_density'))

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(suite())
