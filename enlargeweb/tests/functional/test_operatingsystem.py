from enlargeweb.tests import *

class TestOperatingsystemController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='operatingsystem', action='index'))
        # Test response...
