import unittest

class StukClientTestCase(unittest.TestCase):
    def test_default(self):
        self.assertTrue(True)

def suite():
    suite = unittest.TestSuite()
    suite.addTest(StukClientTestCase('test_default'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
