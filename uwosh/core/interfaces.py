from zope.interface import Interface

class IUWOshTools(Interface):
    """A view that gives access to common tools
    """
    
    def get_last_modified_header():
        """
        """
    
    def set_last_modified_header():
        """
        
        """
        
    def get_copyright_holder():
        """
        
        """
        
    def get_current_year():
        """
        """
        
    def uwosh_login_url():
        """"""
        
    def uwosh_login_without_ssl():
        """"""
        
    def uwosh_home_url():
        """"""
        
    