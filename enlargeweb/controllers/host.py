import logging
import datetime
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from routes import url_for
import webhelpers
import webhelpers.paginate
from enlargeweb.lib.base import BaseController, render
from enlargeweb.model import meta
from enlargeweb.model.srv import Server, Nic, Cpu, Hdd
from enlargeweb.lib.restful_lib import Connection
import simplejson

log = logging.getLogger(__name__)

class HostController(BaseController):
	requires_auth = 'user'
	
	def list(self):
		if not 'page' in request.params:
			page = 1
		else:
			page = request.params['page']
			
		selection = meta.Session.query(Server).order_by(Server.id)
			
		if 'filter_dept' in request.params:
			selection = selection.filter(Server.department == request.params['filter_dept'])
			c.filter_dept = request.params['filter_dept']
				
		c.hosts = webhelpers.paginate.Page(
			selection,
			page = int(page),
			items_per_page = 50)
				
		if 'partial' in request.params:
			return render('host_list_ajax.mako')
		else:
			# Render the full page
			return render('host_list.mako')

	def info(self, id):
		"""# Get the server Info
		http_host = request.environ.get('HTTP_HOST')
		conn = Connection('http://%s/api/' %http_host)
		disks_json = conn.request_get('/add_host', 
				args = {'srv_id': id},
				headers = {'Accept':'text/json'})
		try:
			disks = simplejson.loads(disks_json['body'])
		except Exception, e:
			print '#' * 50
			print 'Exception:', str(e)
		else:
			print '#' * 50
			print disks"""
		c.srv = meta.Session.query(Server).filter(Server.id==id).first()
		c.running_activities, c.history_activities = c.srv.get_activities()
		if 'partial' in request.params:
			c.partial = True
			return render('host_info_ajax.mako')
		else:
			# Render the full page
			return render('host_info.mako')

	def add(self):
		c.srv = Server(None, '', '', '', '', '', False, 0)
		return render('host_edit.mako')

	def edit(self, id):
		c.srv = meta.Session.query(Server).filter(Server.id==id).first()
		return render('host_edit.mako')
		
	def delete(self, id):
		c.srv = meta.Session.query(Server).filter(Server.id==id).first()
		if c.srv:
			meta.Session.delete(c.srv)
			meta.Session.commit()
		return redirect_to(url_for(action = 'list', id = None))
		
	def get_cpu(self):
		cpu_speed_str = request.params.get('cpu_speed')
		if cpu_speed_str:
			cpu_speed = int(cpu_speed_str)
		else:
			cpu_speed = 0
		cpu_arch = str(request.params.get('cpu_arch'))
		cpu_model = str(request.params.get('cpu_model'))
		
		return Cpu(None, cpu_arch, cpu_speed, cpu_model)
		
	def add_cpu(self):
		srv_id = request.params.get('srv_id')
		cpu = self.get_cpu()
		cpu.node_id = int(srv_id)
		if not cpu.arch:
			c.error = 'Please specify CPU architecture'
		else:
			meta.Session.add(cpu)
			meta.Session.commit()
		return redirect_to(url_for(action = 'edit', id = srv_id))
	
	def delete_cpu(self):
		cpu_id = request.params.get('cpu_id')
		srv_id = request.params.get('srv_id')
		cpu = meta.Session.query(Cpu).filter(Cpu.id == cpu_id).one()
		if not cpu:
			c.error = 'No such cpu found.'
		else:
			log.debug('delete CPU %s' % cpu)
			meta.Session.delete(cpu)
			meta.Session.commit()
		return redirect_to(url_for(action = 'edit', id = srv_id))

	def get_nic(self):
		nic_mac = str(request.params.get('nic_mac'))
		srv_id = int(request.params.get('srv_id'))
		nic_ip = str(request.params.get('nic_ip_address'))
		nic_ipmask = str(request.params.get('nic_ip_mask'))
		if request.params.get('nic_ssh_port'):
			nic_ssh_port = int(request.params.get('nic_ssh_port'))
		else:
			nic_ssh_port = 22
		if request.params.get('nic_main'):
			nic_main = True
		else:
			nic_main = False
		nic = Nic(srv_id, nic_mac, nic_ip, nic_ipmask, nic_main, nic_ssh_port)
		return nic

	def add_nic(self):
		srv_id = request.params.get('srv_id')
		nic = self.get_nic()
		meta.Session.add(nic)
		meta.Session.commit()
		return redirect_to(url_for(action = 'edit', id = srv_id))

	def edit_nic(self):
		srv_id = request.params.get('srv_id')
		new_nic = self.get_nic()
		old_nic = meta.Session.query(Nic).filter(Nic.mac == new_nic.mac).one()
		if old_nic:
			old_nic.ip_address = new_nic.ip_address
			old_nic.ip_mask = new_nic.ip_mask
			old_nic.ssh_port = new_nic.ssh_port
			old_nic.main = new_nic.main 
			meta.Session.update(old_nic)
			meta.Session.commit()
				
		return redirect_to(url_for(action = 'edit', id = srv_id))

	def delete_nic(self):
		srv_id = request.params.get('srv_id')
		nic_mac = str(request.params.get('nic_mac'))
		nic = meta.Session.query(Nic).filter(Nic.mac == nic_mac).one()
		meta.Session.delete(nic)
		meta.Session.commit()
		return redirect_to(url_for(action = 'edit', id = srv_id))

	def get_hdd(self):
		hdd_size = request.params.get('hdd_size')
		if hdd_size:
			hdd_size = int(hdd_size)
		else:
			hdd_size = 0
		hdd_device = str(request.params.get('hdd_device'))
		
		return Hdd(None, hdd_device, hdd_size)
		
	def add_hdd(self):
		srv_id = request.params.get('srv_id')
		hdd = self.get_hdd()
		hdd.node_id = int(srv_id)
		if not hdd.device:
			c.error = 'Please specify Disk device'
		else:
			meta.Session.add(hdd)
			meta.Session.commit()
		return redirect_to(url_for(action = 'edit', id = srv_id))

	def edit_hdd(self):
		srv_id = request.params.get('srv_id')
		new_hdd = self.get_hdd()
		old_hdd = meta.Session.query(Hdd).filter(Hdd.device == new_hdd.device).one()
		if old_hdd:
			old_hdd.device = new_hdd.device
			old_hdd.size = new_hdd.size
			meta.Session.update(old_hdd)
			meta.Session.commit()
				
		return redirect_to(url_for(action = 'edit', id = srv_id))
	
	def delete_hdd(self):
		hdd_device = request.params.get('hdd_device')
		srv_id = request.params.get('srv_id')
		hdd = meta.Session.query(Hdd).filter(Hdd.device == hdd_device).one()
		if not hdd:
			c.error = 'No such Disk found.'
		else:
			log.debug('delete HDD %s' % hdd)
			meta.Session.delete(hdd)
			meta.Session.commit()
		return redirect_to(url_for(action = 'edit', id = srv_id))
	
	def save(self):
		srv_id = request.params.get('srv_id')
		log.debug('saving sever with id:%s' % srv_id)
		host_name = request.params.get('host_name')
		host_location = request.params.get('host_location')
		host_owner = request.params.get('host_owner')
		host_type = request.params.get('host_type')
		if host_type.lower() == 'pc':
			host_type = 0
		else:
			host_type = 1
		host_dept = request.params.get('host_dept')
		host_new_dept = request.params.get('host_new_dept')
		if host_new_dept and host_new_dept != host_dept:
			log.debug('use specified new department: %s' % host_new_dept)
			host_dept = host_new_dept
		host_comments = request.params.get('host_comments')

		if srv_id == '':
				srv_id = None

		srv = Server(
				srv_id,
				host_name,
				host_dept,
				host_owner,
				host_location,
				host_comments,
				True,
				0
		)
		log.debug('details: %s' % srv)
		if srv.id:
			srv = meta.Session.merge(srv)
			meta.Session.update(srv)
			meta.Session.commit()
			#this was update, so redirect to info
			return redirect_to(url_for(action = 'info', id = srv.id))
		else:
			meta.Session.add(srv)
			meta.Session.commit()
			#this was the inital commit of new host
			#allow to continue configuration
			return redirect_to(url_for(action = 'edit', id = srv.id))
