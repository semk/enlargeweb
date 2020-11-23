from enlargeweb.tests import *

class TestApplianceController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='appliance', action='index'))
        # Test response...
