from uwosh.core.utils import *
import unittest

class TestUtils(unittest.TestCase):
    """
    """
    
    def test_one_of_these_is_in_is_true(self):
        
        x = [1,2,3,4]
        y = [3,4,5,6]
        z = [9,10,11]
        self.assertEqual(one_of_these(x).is_in(y), True)
        
    def test_one_of_these_is_in_is_false(self):
        x = [1,2,3,4]
        y = [3,4,5,6]
        z = [9,10,11]
        self.assertEqual(one_of_these(x).is_in(z), False)
        
    def test_each_one_of_these_is_in(self):
        x = [1,2,3]
        y = [1,2,3,4,5]
        self.assertEqual(each_one_of_these(x).is_in(y), True)
        
    def test_each_one_of_these_is_in_failure(self):
        x = [1,2,3,7]
        y = [1,2,3,4,5]
        self.assertEqual(each_one_of_these(x).is_in(y), False)
        
    def test_each_one_of_these_is_not_in(self):
        x = [1,2,3]
        y = [4,5,6]
        self.assertEqual(each_one_of_these(x).is_not_in(y), True)
        
    def test_each_one_of_these_is_not_in_failure(self):
        x = [1,2,3,4]
        y = [4,5,6]
        self.assertEqual(each_one_of_these(x).is_not_in(y), False)
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUtils))
    return suite