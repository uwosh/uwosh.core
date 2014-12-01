from urllib import *
from parsing import PrimitiveParser

class RemoteMethod:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.parser = PrimitiveParser()

    def __call__(self, **kwargs):
        data = {
            'method': self.name
        }
        for key, value in kwargs.items():
            data[key] = value

        result = urlopen(self.url, urlencode(data)).read()

        if result is not None and len(result) > 0:
            return self.parser.parse(result)
        else:
            return None    
                
class RemoteService:
    """
    Used to call remote methods of views that are implemented MethodView

    """         
    def __init__(self, url):
        self.url = url
        
    def __getattr__(self, name):
        builtin =  name.startswith('__') and name.endswith('__')
        if builtin:
            return self.__dict__[name]
        
        return RemoteMethod(name, self.url)