from Products.Five.browser import BrowserView
from uwosh.core.parsing import PrimitiveParser, NoneType

class MethodView(BrowserView):
    """
    Use this view if you have methods defined in your browser pages that you want to call....
    Much like xml-rpc, but will only work with python
    This class is intended to be inherited by a view
    
    >>> class MyMethods(MethodView):
    ...   def __init__(self):
    ...     class request:
    ...       pass   
    ...     self.request = request()
    ...   def testMethod(self, **kwargs):
    ...     return "Hello, World"
    ...   def methodNotFound(self):
    ...     return "Error"
    >>> mv = MyMethods()
    >>> mv.request.form = {'method': 'testMethod'}
    >>> mv()
    'Hello, World'
    
    >>> mv.request.form = {'method': 'oskdf'}
    >>> mv()
    'Error'
    """
    
    trusted_domains = None
    parser = PrimitiveParser()
    
    def check_is_from_trusted_domain(self):
        if self.trusted_domains is None:
            return True
        else:
            for domain in self.trusted_domains:
                if self.request["REMOTE_ADDR"] == domain:
                    return True
                    
            raise Exception, "Not a trusted domain."
            
    def result_handler(self, result):
        """
        This wraps strings in quotes so the parser can know that they should be handled as strings.
        """
        if type(result) == str:
            return '"%s"' % result
        else:
            return result
        
            
    def __call__(self):
    
        if self.check_is_from_trusted_domain():
        
            form = self.request.form
            method = form.get('method', None)
            result = None

            if hasattr(self, method):
                method = getattr(self, method)

                for key, arg in form.items():
                    value = self.parser.parse(arg)
                    if value.__class__ == NoneType:
                        value = str(arg)
                    form[key] = value

                del(form['method'])
                
                return self.result_handler(method(**form))
            else:
                return self.methodNotFound()
                
                
    def methodNotFound(self):
        """
        Override this method to handle incorrect method calls
        """
        raise Exception, "Can not find method"