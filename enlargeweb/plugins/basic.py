# EnlargeWeb source code
# Licenced under GPLv3
# Stanislav Yudin
import os, sys
from enlargeweb.model.act import Activity
from enlargeweb.model.srv import Server
from enlargeweb.model import meta
from pylons import config

class BasicPlugin(object):
	def init(self, log, args):
		self.log = log
		self.args = args
		self.target = meta.Session.query(Server).filter(Server.id == int(args['host_id'])).with_lockmode('update').one()
		self.activity = meta.Session.query(Activity).filter(Activity.id == int(args['activity_id'])).with_lockmode('update').one()
		self.log.info('Plugin initialization for activity:%s' % self.activity.id)
		
	def put_log(self, msg):
		self.log.info(msg)
		self.activity.put_log(msg)
