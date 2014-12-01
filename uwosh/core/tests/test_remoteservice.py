from uwosh.core import remoteservice
import unittest

class TestRemoteService(unittest.TestCase):
    """

    """
    
    def test_should_return_data_correctly(self):
        class mocked_urlopen:
            def __init__(self, url, args):
                pass

            def read(self):
                return "'Hello, Mike'"
                
        remoteservice.urlopen = mocked_urlopen
        rs = remoteservice.RemoteService("http://fakeurl/")
        
        self.assertEqual(rs.hello(name="Mike"), "Hello, Mike")
        
    def test_should_return_complex_result_correctly(self):
        class mocked_urlopen:
            def __init__(self, url, args):
                pass

            def read(self):
                return [1,2,3, {'hi': 'no'}]
                
        remoteservice.urlopen = mocked_urlopen
        rs = remoteservice.RemoteService("http://fakeurl/")
        
        self.assertEqual(rs.hello(name="Mike"), [1,2,3, {'hi': 'no'}])
        
    def test_remote_service_should_get_correct_request_url(self):
        rs = remoteservice.RemoteService("http://fakeurl/")        
        self.assertEqual(rs.url, "http://fakeurl/")
    
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRemoteService))
    return suite