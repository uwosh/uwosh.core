from uwosh.core import remoteservice
import unittest

class TestTools(unittest.TestCase):
    """

    """
    
    
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestTools))
    return suite