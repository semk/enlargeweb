from enlargeweb.tests import *

class TestXmlrpcController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='xmlrpc', action='index'))
        # Test response...
