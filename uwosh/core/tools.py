from zope.interface import implements
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.i18n.locales import locales, LoadLocaleError
from zope.component import getMultiAdapter
from plone.memoize.view import memoize, memoize_contextless

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from plone.app.layout.navigation.root import getNavigationRoot

from interfaces import IUWOshTools
from datetime import datetime
from DateTime import DateTime

class UWOshTools(BrowserView):
    """
    Utility methods for UW Oshkosh stuff
    remember that if you add a method here,
    you'll need to add it to the interface too
    """
    implements(IUWOshTools)

    def __init__(self, context, request):
        super(UWOshTools, self).__init__(context, request)
        
        self.portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
                                        
    @memoize_contextless
    def get_current_year(self):
        return datetime.now().year
    
    @memoize_contextless    
    def get_copyright_holder(self):
        return getattr(self.portal_state.portal(), 'copyright_holder', None)

    @memoize_contextless    
    def get_help_url(self):
        return getattr(self.portal_state.portal(), 'uwosh_help_url', None)

    def set_last_modified_header(self):
        """
        Just set the field "last_modified_header" on
        the portal root.  Getting the header will
        check that variable for the header info.
        """
        
        portal_root = self.portal_state.portal()
        portal_root.last_modified_header = DateTime()

    @memoize
    def uwosh_login_url(self):
        portal_root = self.portal_state.portal()
        if getattr(portal_root, 'uwosh_login_without_ssl', False):
            return self.context.absolute_url() + "/login_form"
        else:
            return self.context.absolute_url().replace('http://','https://') + "/login_form"

    @memoize_contextless
    def uwosh_login_without_ssl(self):
        portal_root = self.portal_state.portal()
        
        return getattr(portal_root, 'uwosh_login_without_ssl', False)
            
    @memoize_contextless
    def uwosh_home_url(self):
        portal_root = self.portal_state.portal()
        if portal_root.getProperty('use_uwosh_home_url', False):
            return portal_root.getProperty('uwosh_home_url', None)
        else:
            return self.portal_state.portal_url()

    @memoize
    def get_last_modified_header(self):
        """
        check the context modified date and
        check if there is a last_modified_header
        in the portal root and then compare
        
        Might need to be more complicated than this
        because each page could possible do this type
        of approach instead of just the portal root
        handling it.
        """
        context_modified_date = self.context.modified()
        portal_root = self.portal_state.portal()
        
        if hasattr(portal_root, 'last_modified_header'):
            portal_last_modified = portal_root.last_modified_header
            
            if portal_last_modified > context_modified_date:
                context_modified_date = portal_last_modified
        
        if (DateTime() - context_modified_date) > 1:
            # If it is older than a day, refresh
            # maybe make this some kind of property that can be
            # customized?
            portal_root.last_modified_header = DateTime()
            context_modified_date = portal_root.last_modified_header
            
        return context_modified_date
