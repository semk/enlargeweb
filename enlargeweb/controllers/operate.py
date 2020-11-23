import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from routes import url_for
from enlargeweb.lib.base import BaseController, render
from enlargeweb.lib.plugins import get_plugins, PluginOption
from enlargeweb.lib.worker import getPluginInstance, spawn
from enlargeweb.lib.helpers import get_current_user
from enlargeweb.model import meta
from enlargeweb.model.srv import Server
from enlargeweb.model.act import Activity
from enlargeweb.model.appl import Appliance


class OperateController(BaseController):
	requires_auth = True

	def render_1(self):
		#write list of classes
		c.appl_types = get_plugins('enlargeweb/plugins')
		return render('appliance.mako')

	def render_2(self):
		c.appliances =  meta.Session.query(Appliance).filter(Appliance.plugin_id == c.appl_plugin_id).order_by(Appliance.name)
		return render('appliance.mako')

	def appliance(self, id, stage = None):
		c.srv = meta.Session.query(Server).filter(Server.id==id).one()
		
		#check if server is busy with something?
		r, h = c.srv.get_activities()
		if len(r)>0:
			c.conflict = ('activity', r[0].id, id)
		
		c.stage = stage
		c.partial = True
		print '--------------- APPLIANCE STAGE %s' % stage
		if stage is None or len(str(stage)) == 0:
			return self.render_1()
		elif stage == 'stage_2':
			#received type, getting names
			c.appl_plugin_id = request.params.get('appl_plugin_id')
			print '------------- SELECTED PLUGIN ID', c.appl_plugin_id
			if not c.appl_plugin_id:
				c.error = 'Pleas select type.'
				return self.render_1()
			return self.render_2()
		elif stage == 'stage_3':
			c.appl_plugin_id = request.params.get('appl_plugin_id')
			c.appl_id = request.params.get('appl_id')
			print '------------- SELECTED APPL ID', c.appl_id
			if not c.appl_id or not c.appl_plugin_id:
				c.error = 'Please select appliance.'
				return self.render_2()
				
			#get the appliance
			activity = OperateController.spawn_activity(get_current_user().login, c.srv.id, c.appl_id, c.appl_plugin_id)
			if not activity:
				return redirect_to('/error?code=1')
			#show activity
			return redirect_to(url_for(controller='activity', action = 'info', id = activity.id, stage = None))
	
	@classmethod
	def spawn_activity(cls, owner, host_id, appl_id, appl_plugin_id):
		appl = meta.Session.query(Appliance).filter(Appliance.id == int(appl_id)).one()
		args = {}
		#copy args from appliance
		for p in appl.properties:
			args[p.name] = p.value
		args['appl_name'] = appl.name
		args['owner'] = owner
		args['host_id'] = host_id
		args['appl_plugin_id'] = appl_plugin_id
		args['appl_id'] = appl_id
		logging.info('ARGS: %s' % args)
		#spawn activity
		activity = spawn(args['appl_plugin_id'], 'Deployment of appliance %s' % args['appl_name'], args)
		return activity
