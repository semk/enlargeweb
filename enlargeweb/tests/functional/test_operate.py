from enlargeweb.tests import *

class TestOperateController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='operate', action='index'))
        # Test response...
