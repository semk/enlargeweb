import logging
import webhelpers.paginate
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from enlargeweb.model import meta
from enlargeweb.model.appl import Appliance
from enlargeweb.model.srv import ServerAppliance, Server
from enlargeweb.model.prop import ApplianceProperty
from sqlalchemy.sql.expression import desc
from enlargeweb.lib.base import BaseController, render
from enlargeweb.lib.plugins import get_plugins, PluginOption
from enlargeweb.lib.worker import getPluginInstance
from routes import url_for

log = logging.getLogger(__name__)

class ApplianceController(BaseController):
	requires_auth = True

	def list(self):
		if not 'page' in request.params:
			page = 1
		else:
			page = request.params['page']
		c.appliances = webhelpers.paginate.Page(
			meta.Session.query(Appliance).order_by(desc(Appliance.name)),
			page = int(page),
			items_per_page = 15)
		
		if 'partial' in request.params:
			return render('appliance_list_ajax.mako')
		else:
			# Render the full page
			return render('appliance_list.mako')

	def info(self, id):
		c.appl = meta.Session.query(Appliance).filter(Appliance.id == id).one()
		refs = meta.Session.query(ServerAppliance).filter(ServerAppliance.appliance_id == id)
		ids = []
		for r in refs:
			 ids.append(r.node_id)
		c.hosts = meta.Session.query(Server).filter(Server.id.in_(ids)).all()
		return render('appliance_info.mako')

	def add(self):
		c.appl = Appliance(None, '', '', '', '', None)
		c.plugins = get_plugins('enlargeweb/plugins')
		return render('appliance_edit.mako')

	def edit(self, id, stage = None):
		print '------:APPL:------- edit appl received', c.appl
		c.appl = meta.Session.query(Appliance).filter(Appliance.id==id).first()
		if not c.appl:
			c.appl = Appliance(None, '', '', '', '', None)
		c.stage = stage
		print '------:APPL:------- edit appl used', c.appl
		print '------:APPL:------- stage', c.stage
		if stage is None or len(str(stage)) == 0:
			#first stage, show appliance name, arch and type selection
			return render('appliance_edit.mako')
		elif stage == 'stage_2':
			return self.render_edit_2()

	def get_appl(self):
		print '------:APPL:------- reading user input'
		c.appl_id = request.params.get('appl_id')
		print '------:APPL:------- id', c.appl_id
		c.appl_plugin_id = request.params.get('appl_plugin_id')
		print '------:APPL:------- plugin_id', c.appl_plugin_id
		if not c.appl_plugin_id:
			c.error = 'Please specify type.'
			return False

		c.appl_name = request.params.get('appl_name')
		print '------:APPL:------- name', c.appl_name
		if not c.appl_name:
			c.error = 'Please specify name.'
			return False

		c.appl_description = request.params.get('appl_description')
		print '------:APPL:------- desc', c.appl_description
		c.appl_arch = request.params.get('appl_arch')
		print '------:APPL:------- arch', c.appl_arch
		return True
		
	def get_appl_deps(self):
		print '------:APPL:------- reading appl depend list'
		result = []
		for i in range(0, 9):
			value = request.params.get('depend%s' % i)
			print '------:APPL:------- %s = %s' % ( 'depend%s' % i, value )
			if value and len(value)>0:
				result.append(int(value))
		print '------:APPL:------- depend on', result
		return result

	def render_edit_2(self):
		#save name, arch, desc and type
		if not self.get_appl():
			c.stage = None
			return render('appliance_edit.mako')

		#get options for selected type
		plugins = get_plugins('enlargeweb/plugins')
		current_plugin = None
		tmp_options = []
		for p in plugins:
			print '------:APPL:------- check type', p.type_id, c.appl_plugin_id
			if p.type_id == c.appl_plugin_id:
				tmp_options = p.options
				current_plugin = getPluginInstance(p.type_id)
				break
		print '------:APPL:------- tmp options', tmp_options
		if not tmp_options:
			c.error = 'Failed to query options.'
			return render('appliance_edit.mako')

		#populate enumerational options
		c.options = []
		for opt_desc, opt_name, opt_type, opt_func in tmp_options:
			if opt_type == 'enum' and opt_func:
				variants = getattr(current_plugin, opt_func)()
				print '------------ VARIANTS FOR %s : %s' % (opt_name, variants)
				c.options.append( PluginOption(opt_name, opt_desc, opt_type, variants) )
			elif opt_type == 'text' and opt_func:
				c.options.append( PluginOption(opt_name, opt_desc, opt_type, opt_func) )
			else:
				c.options.append( PluginOption(opt_name, opt_desc, opt_type, '') )
		print '------:APPL:------- options', c.options
		
		#populate list of available appliances
		c.appls = meta.Session.query(Appliance).all()
		return render('appliance_edit.mako')

	def delete(self, id):
		c.appl = meta.Session.query(Appliance).filter(Appliance.id==id).first()
		if c.appl:
			meta.Session.delete(c.appl)
			meta.Session.commit()
		return redirect_to(url_for(action = 'list', id = None))

	def save(self):
		if not self.get_appl():
			return render('appliance_edit.mako')

		#save dependences
		depend_on_list = self.get_appl_deps()

		if c.appl_id == '':
			c.appl_id = None
		
		#get option names to read values from request params
		plugins = get_plugins('enlargeweb/plugins')
		current_plugin = None
		options = None
		icon = None
		for p in plugins:
			if p.type_id == c.appl_plugin_id:
				options = p.options
				icon = p.icon
				break
		if not options:
			c.error = 'Failed to query options.'
			return render('appliance_edit.mako')
		
		#Creating new appliance
		appl = Appliance(
			c.appl_id,
			c.appl_name,
			c.appl_description,
			c.appl_arch,
			c.appl_plugin_id,
			icon
		)
		if appl.id:
			appl = meta.Session.merge(appl)
			meta.Session.update(appl)
		else:
			meta.Session.add(appl)
		meta.Session.commit()

		print '------:APPL:------- SAVED %s' % str(appl)

		#create ApplicanceProperty for each read option value
		appl_props = []
		for opt_desc, opt_name, opt_type, opt_func in options:
			value = request.params.get(opt_name)
			if not value:
				value = ''
			if opt_type == 'enum' and len(value) <= 0:
				c.error = 'Please specify %s.' % opt_name
				return self.render_edit_2()
				
			#try to get existing property
			if appl.id and not appl.get_prop(opt_name) is None:
				prop = appl.get_prop_inst(opt_name)
				prop.value = value
			else:
				prop = ApplianceProperty(appl.id, opt_name, opt_desc, value)
			print '------:APPL:------- PROP %s' % str(prop)
			meta.Session.add(prop)
			
		#add dependences
		for dep_appl_id in depend_on_list:
			dep_appl = meta.Session.query(Appliance).filter(Appliance.id == int(dep_appl_id)).one()
			appl.depends_on.append( dep_appl )

		meta.Session.commit()
		print '------:APPL:------- DONE SAVING'
		return redirect_to(url_for(action = 'info', id = appl.id))
