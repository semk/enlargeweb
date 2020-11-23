from enlargeweb.tests import *
from enlargeweb.lib.restful_lib import Connection
import simplejson, logging

log = logging.getLogger(__name__)

class TestApiController(TestController):
	def test_list_hosts(self):
		client = Connection('http://localhost:8080/api/')
		hosts_json = client.request_get('/list_hosts', headers={'Accept':'text/json'})
		hosts = simplejson.loads(hosts_json['body'])
		assert( len(hosts)>0 )
		for h in hosts:
			assert(int(h['id']) > 0 )
			assert(len(h['name'])>0)
			assert(len(h['type'])>0)
			assert(len(h['os'])>0)
			assert(isinstance(h['online'], bool))
			assert(len(h['owner'])>0)
			print log.debug(h)
			
	def test_list_appl(self):
		client = Connection('http://localhost:8080/api/')
		appls_json = client.request_get('/list_appliances', headers={'Accept':'text/json'})
		appls = simplejson.loads(appls_json['body'])
		for a in appls:
			assert( int(a['id'])>0)
			assert(len(a['arch'])>0)
			assert(len(a['plugin_id'])>0)
			assert(len(a['icon'])>0)

"""	def test_deploy_appliance(self):
		client = Connection('http://localhost:8080/api/')
		act_json = client.request_get(	'/deploy_activity', 
										args = { 'host_id': 2, 'appl_id' : 4, 'owner' : 'test' },
										headers = {'Accept':'text/json'}
									)
		act = simplejson.loads(act_json['body'])
		assert( act[0] > 0 ) # activity id
		assert( len(act[1]) > 0 ) # activity description
		assert( len(act[2]) > 0 ) # start time
		assert( act[3] > 0 ) # child process PID
    """
    
