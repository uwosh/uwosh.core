from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
      
def isProductInstalled(product_name):
    site = getSite()
    qi = getToolByName(site, 'portal_quickinstaller')
    return qi.isProductInstalled(product_name)
    

class one_of_these:
    """
    just a nice class to make it readable when evaluating lists....
    
    >>> from uwosh.core.utils import one_of_these
    >>> x = [1,2,3]
    >>> y = [3,4,5]
    >>> z = [8,9,10]
    
    >>> one_of_these(x).is_in(y)
    True
    
    >>> one_of_these(y).is_in(z)
    False
    """
    def __init__(self, lst):
        self.lst = lst
        
    def is_in(self, otherlist):
        for item in otherlist:
            if item in self.lst:
                return True
        return False

class none_of_these:
    """
    
    >>> from uwosh.core.utils import none_of_these
    >>> x = [1,2,3]
    >>> y = [3,4,5]
    >>> z = [8,9,10]
    
    >>> none_of_these(x).are_in(z)
    True
    
    >>> none_of_these(x).are_in(y)
    False
    
    """
    
    def __init__(self, lst):
        self.lst = lst
        
    def are_in(self, otherlist):
        for item in self.lst:
            if item in otherlist:
                return False
        return True

class each_one_of_these:
    """
    
    >>> from uwosh.core.utils import each_one_of_these
    >>> x = [1,2,3]
    >>> y = [1,2,3,4,5]
    >>> z = [8,9,10]
    
    >>> each_one_of_these(x).is_in(y)
    True
    
    >>> each_one_of_these(y).is_in(x)
    False
    
    >>> each_one_of_these(x).is_not_in(z)
    True
    
    >>> each_one_of_these(x).is_not_in(y)
    False
    
    """
    def __init__(self, lst):
        self.lst = lst
        
    def is_not_in(self, otherlist):
        for item in self.lst:
            if item in otherlist:
                return False
                
        return True
        
    def is_in(self, otherlist):
        for item in self.lst:
            if item not in otherlist:
                return False
                
        return True
        
class retrieve:
    def __init__(self, item):
        self.item = item
        
    def get_properties(self):
        return getattr(getToolByName(getSite(), 'portal_properties'), self.item, None)
    def set_properties(self, value):
        raise Exception("You are not allowed to set this property like this")
        pass
    properties = property(get_properties, set_properties)
            
