from uwosh.core.utils import *
import unittest

class TestParser(unittest.TestCase):
    """
    Test parsing is done right...
    """
    
    def test_parses_int_correctly(self):
        parser = PrimitiveParser()
        
        self.failUnless(1234 == parser.parse("1234"))
        
    def test_parses_float_correctly(self):
        parser = PrimitiveParser()
        self.failUnless(123.456 >= parser.parse("123.456") and parser.parse("123.456") <= 123.4561)
        
    def test_parses_None_correctly(self):
        parser = PrimitiveParser()
        self.failUnless(parser.parse("None") is None)
        
    def test_parses_string_correctly(self):
        parser = PrimitiveParser()
        self.failUnless(parser.parse("'Hello, world'") == "Hello, world")
        
    def test_parses_list_correctly(self):
        parser = PrimitiveParser()
        self.failUnless(parser.parse("[1, 2, 'hi', None, True]") == [1, 2, 'hi', None, True])
        
    def test_parse_boolean_correctly(self):
        parser = PrimitiveParser()
        self.failUnless(parser.parse("True") and not parser.parse("False"))
        
    def test_parses_dict_correctly(self):
        parser = PrimitiveParser()
        self.failUnless(parser.parse("""{'x': 1, 'y': 2, 3 : 'z'}""") == {'x':1, 'y':2, 3:'z'})
        
    def test_parses_super_crazy_complex_example_correctly(self):
        parser = PrimitiveParser()
        test_string = """
        {
            'x': 5,
            'y': 6,
            123: 'sldfkn',
            'z': True,
            'a': [1,2,3,4],
            'b': {
                1:1,
                2:2,
                '3': '3'
            },
            'c': [1,2,3,'sdlkfns', {
                '123':4,
                '456':5,
                'list': [1,2,3,4,5]
            }]
        }
        """
        result = {
            'x': 5,
            'y': 6,
            123: 'sldfkn',
            'z': True,
            'a': [1,2,3,4],
            'b': {
                1:1,
                2:2,
                '3': '3'
            },
            'c': [1,2,3,'sdlkfns', {
                '123':4,
                '456':5,
                'list': [1,2,3,4,5]
            }]
        }
        self.failUnless(parser.parse(test_string) == result)
    
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestParser))
    return suite
