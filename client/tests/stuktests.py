import unittest
import stuk

class StukClientTestCase(unittest.TestCase):
    def test_default(self):
        self.assertTrue(True)

"""
Test suite para probar la encriptación/desencriptado a partir de un par de claves.
.keys/
├── it_rsa.pem
└── it_rsa.pub
"""
class StukCryptoTestCase(unittest.TestCase):
    def test_encryptation(self):
        self.assertTrue(True)
    def test_decryptation(self):
        self.assertTrue(True)

"""
Test suite 
"""
def suite():
    suite = unittest.TestSuite()
    suite.addTest(StukClientTestCase('test_default'))
    suite.addTest(StukCryptoTestCase('test_encryptation'))
    suite.addTest(StukCryptoTestCase('test_decryptation'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
