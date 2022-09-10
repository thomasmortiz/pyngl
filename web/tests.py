import unittest

class TestRouteMethods(unittest.TestCase):

    def setUp(self):
        return

    def test_index_route(self):
        return

    def tearDown(self):
        return    

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestRouteMethods('test_index_route'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
