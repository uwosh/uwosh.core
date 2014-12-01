import shlex
import StringIO

def is_closing_list(v):
    return v in ["]", ")"]    
    
def is_opening_list(v):
    return v in ["[", "("]
    
def is_opening_dict(v):
    return v == "{"
def is_closing_dict(v):
    return v == "}"
    
def is_int(v):
    try:
        val = int(v)
        return True
    except:
        return False
        
def is_float(v):
    try:
        val = float(v)
        return True
    except:
        return False
        
class NoneType:
    pass

class ParseError(Exception):
    pass

class PrimitiveParser:
    """
    A class that parses a python value from a string
    It does not allow any operations to be performed inside the string.
    That is why we don't use the exec or eval methods to do it.
    This ensures safe evaluation of python values from a string
    Much like json parsing is done...
    
    >>> PrimitiveParser().parse("{3:'lsdkfn', 'lsdkfn':45654}")
    {3:"lsdkfn", 'lsdkfn':45654}
    """
    
    def __init__(self, value=None):
        if value is not None:
            self.tokenizer = shlex.shlex(StringIO.StringIO(value))
        else:
            self.tokenizer = None
        
    def set_value_to_parse(self, value):
        self.tokenizer = shlex.shlex(StringIO.StringIO(value))
        self.unparsed_value = value
        
    def __call__(self, value_to_parse=None):
        
        if value_to_parse is not None:
            self.set_value_to_parse(value_to_parse)
            
        if self.tokenizer is not None:
            return self.parse()
        else:
            raise Exception, "You have not set a value to parse yet!"

    def parse_it(self, token):
        if is_opening_list(token):
            return self.parse_list(self.tokenizer.get_token(), [])
        elif is_opening_dict(token):
            return self.parse_dict(self.tokenizer.get_token(), {})
        elif token.startswith("'") or token.startswith('"'):
            return token.strip('"').strip("'")
        elif token == "False" or token == "True":
            return eval(token)
        elif token == "None":
            return None
        elif is_int(token):
            return int(token)
        elif is_float(token):
            return float(token)
        else:
            return NoneType()

    def parse_dict(self, token, ret):
        if is_closing_dict(token) or len(token) == 0:
            return ret
         
        key = self.parse_it(token)
        if key.__class__ == NoneType:
            raise ParseError, "Can not parse key of dictionary."
        
        token = self.tokenizer.get_token()
        if token != ":":
            raise ParseError, "Error parsing dictionary"
            
        token = self.tokenizer.get_token()
        value = self.parse_it(token)
        if value.__class__ == NoneType:
            raise ParseError, "Can not parse value of key %s for dictionary." % key
            
        ret[key] = value
        
        token = self.tokenizer.get_token()
        
        if token == ",":
            return self.parse_dict(self.tokenizer.get_token(), ret)
        else:
            return ret
            
    def parse_list(self, token, ret):
        if is_closing_list(token) or len(token) == 0:
            return ret

        val = self.parse_it(token)
        if val.__class__ == NoneType:
            raise ParseError, "Error parsing list"
            
        ret.append(val)
            
        token = self.tokenizer.get_token()

        if token == ",":
            return self.parse_list(self.tokenizer.get_token(), ret)
        else:
            return ret
            
    def parse(self, value_to_parse=None):
        """
        setup recursion...
        """
        if value_to_parse is not None:
            self.set_value_to_parse(value_to_parse)
            
        if self.tokenizer is not None:
            return self.parse_it(self.tokenizer.get_token())
        else:
            raise Exception, "You have not set a value to parse yet!"