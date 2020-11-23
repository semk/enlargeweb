from enlargeweb.tests import *

class TestHostController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='host', action='index'))
        # Test response...
