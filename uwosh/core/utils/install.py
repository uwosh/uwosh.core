from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
import has

class these:
    """
    helpers methods to install various things.
    
    >>> from uwosh.core.utils import install
    >>> install.these(['uwosh.default', 'uwosh.themebase']).dependencies()
    """
    
    
    def __init__(self, list_of_things_to_install=[]):
        self.what_to_install = list_of_things_to_install
        
    def dependencies(self, reinstall=False):
        portal = getSite()
        qi = getToolByName(portal, 'portal_quickinstaller')
        for product in self.what_to_install:
            if not has.product(product).installed():
                if has.product(product).installable():
                    qi.installProduct(product)
                else:
                    raise "Product %s not installable" % product 
            elif reinstall:
                qi.reinstallProducts([product])
        
    def vocabularies(self):
        portal = getSite()
        
        if not has.product('ATVocabularyManager').installed():
            raise "ATVocabularyManager is not installed!"
        
        atvm = getToolByName(portal, 'portal_vocabularies')

        for vkey in self.what_to_install.keys():
            # create vocabulary if it doesnt exist:
            vocabname = vkey
            if not hasattr(atvm, vocabname):
                #print >>out, "adding vocabulary %s" % vocabname
                atvm.invokeFactory('SimpleVocabulary', vocabname)
            vocab = atvm[vocabname]

            if len(vocab.getFolderContents()) < 2:
                for (ikey, value) in self.what_to_install[vkey]:
                    if not hasattr(vocab, ikey):
                        vocab.invokeFactory('SimpleVocabularyTerm', ikey)
                        vocab[ikey].setTitle(value)
                        
class this:
    """
    to install just one dependency
    
    >>> from uwosh.core.utils import install
    >>> install.this('uwosh.default').dependency()
    """
    def __init__(self, what):
        self.what = what
        
    def dependency(self):
        portal = getSite()
        qi = getToolByName(portal, 'portal_quickinstaller')
        if not qi.isProductInstalled(self.what):
            if qi.isProductInstallable(self.what):
                qi.installProduct(self.what)
            else:
                raise "Product %s not installable" % self.what