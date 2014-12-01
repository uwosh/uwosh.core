from uwosh.core.utils import MethodView
import unittest

class FakeRequest:
    
    def __init__(self):
        self.__dict__['REMOTE_ADDR'] = 'localhost'
        self.__dict__['form'] = {
            'method': 'sayHelloTo'
        }
    
    def __getattr__(self, name):
        return self.__dict__[name]
    
    def __setattr__(self, name, value):
        self.__dict__[name] = value
        


class TestMethodView(unittest.TestCase):
    """

    """
    
    def setUp(self):
        class MyMethods(MethodView):
            def __init__(self):
                self.request = FakeRequest()
            
            def sayHelloTo(self, name="Joe", **kwargs):
                return "Hello, %s" %name
            
            def methodNotFound(self):
                return "Error"

        self.mv = MyMethods()
        self.mv.trusted_domains = ['localhost']
        self.mv.request.form = {'method': 'sayHelloTo'}
    
    def test_should_raise_exception_if_not_from_trusted_domain(self):
        self.mv.trusted_domains = []
        self.assertRaises(Exception, self.mv)
        
    def test_should_not_raise_exception_if_from_trusted_domain(self):
        self.mv.request.form['name'] = 'Mike'
        self.mv()
        
    def test_should_raise_exception_if_method_not_found(self):
        self.mv.request.form['method'] = 'sayNothing'
        self.assertRaises(Exception, self.mv)
        
    def test_should_return_the_correct_data(self):
        self.assertEqual(self.mv.sayHelloTo(name="Mike"), "Hello, Mike")
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestMethodView))
    return suite