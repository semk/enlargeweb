import logging
import datetime
import simplejson
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from enlargeweb.model import meta
from enlargeweb.model.srv import Server, Nic, BootEntry, Hdd, Cpu
from enlargeweb.model.appl import Appliance
from enlargeweb.lib.base import BaseController, render
from pylons.decorators import rest
from enlargeweb.controllers.operate import OperateController
from enlargeweb.lib.server_info import ServerInfo

log = logging.getLogger(__name__)

class ApiController(BaseController):
	requires_auth = False
	
	def __before__(self):
		BaseController.__before__(self)
		self.format = request.headers['Accept']
		print ' #### Accept: %s ####' % self.format
	
	@rest.restrict('GET')
	def disable_boot(self, id):
		if meta.Session.query(Server).filter(Server.id == id).count() == 0:
			return 'No host with id:%s\n' % id
		
		node = meta.Session.query(Server).filter(Server.id == id).one()
		if meta.Session.query(BootEntry).filter(BootEntry.mac == node.get_main_nic().mac).count() > 0:
			boot_entry = meta.Session.query(BootEntry).filter(BootEntry.mac == node.get_main_nic().mac).one()
			meta.Session.delete(boot_entry)
			meta.Session.commit()
			return 'Boot for host:%s(%s) mac:%s removed on %s\n' % ( node.name, node.id, boot_entry.mac, datetime.datetime.now() )
		else:
			return 'Boot entry not specified for host:%s(%s)\n' % (node.name, node.id)
	
	def __format(self, obj):
		if self.format == 'text/json':
			return simplejson.dumps(obj)
		elif self.format == 'text/xml':
			return '<error>Not supported</error>'
	
	@rest.restrict('GET')
	def list_hosts(self):
		hosts = []
		for host in meta.Session.query(Server):
			hosts.append( { 'id'	:	host.id, 
							'name'	:	host.name,
							'dept'	:	host.department,
							'loc'	:	host.location,
							'comments': host.comments,
							'owner' :	host.owner,
							'type'	:	host.get_type(),
							'arch'	:	host.get_arch(),
							'os'	:	host.get_os(),
							'online':	host.online } )
							
		return self.__format(hosts)
	
	@rest.restrict('GET')
	def deploy_appliance(self):
		appl_id = request.params.get('appl_id')
		host_id = request.params.get('host_id')
		owner = request.params.get('owner')
		print ' #### API: deploy_appliance(host_id=%s, appl_id=%s, owner=%s) ###' % ( host_id, appl_id, owner)
		appl = meta.Session.query(Appliance).filter(Appliance.id == int(appl_id)).one()
		host = meta.Session.query(Server).filter(Server.id == int(host_id)).one()
		activity = OperateController.spawn_activity(owner, host.id, appl.id, appl.plugin_id)
		return self.__format(
			(	activity.id, 
				activity.description,
				str(activity.start_time),
				activity.proc_id
			)
		)
		
	@rest.restrict('GET')
	def list_appliances(self):
		appls = []
		for appl in meta.Session.query(Appliance):
			appls.append({
						'id' 		: appl.id,
						'desc'		: appl.description,
						'arch'		: appl.arch,
						'plugin_id'	: appl.plugin_id,
						'icon'		: appl.icon
						})
		return self.__format(appls)

	@rest.restrict('GET')
	def add_all(self):
		msg = []
		msg.append(self.add_host())
		msg.append(self.add_cpu())
		msg.append(self.add_nic())
		msg.append(self.add_disk())
		return self.__format(msg)

	@rest.restrict('GET')
	def add_host(self):
		host_name = request.params.get('host_name')
		host_dept = request.params.get('host_dept')
		host_owner = request.params.get('host_owner')
		host_location = request.params.get('host_location')
		host_comments = request.params.get('host_comments')
		
		type = request.params.get('host_type')
		if host_type.lower() == 'pc':
			host_type = 0
		else:
			host_type = 1
		
		host = Server(None, 
						host_name, 
						host_dept, 
						host_owner, 
						host_location, 
						host_comments, 
						True, 
						host_type)
		meta.Session.add(host)
		meta.Session.commit()
		return 'Host %s added successfully' % host_name

	@rest.restrict('GET')
	def add_cpu(self):
		srv_id = int(request.params.get('srv_id'))
		cpu_speed_str = request.params.get('cpu_speed')
		if cpu_speed_str:
			cpu_speed = int(cpu_speed_str)
		else:
			cpu_speed = 0
		cpu_arch = str(request.params.get('cpu_arch'))
		cpu_model = str(request.params.get('cpu_model'))
		
		cpu = Cpu(None, cpu_arch, cpu_speed, cpu_model)
		cpu.node_id = srv_id
		meta.Session.add(cpu)
		meta.Session.commit()
		return 'Cpu Added successfully id: %d' %cpu.id

	@rest.restrict('GET')
	def del_cpu(self):
		print 'API ==> Deleting CPU information'
		cpu_id = int(request.params.get('cpu_id'))
		cpu = meta.Session.query(Cpu).filter(Cpu.id == cpu_id).one()
		if not cpu:
			return 'No such CPU'
		meta.Session.delete(cpu)
		meta.Session.commit()
		return 'Cpu with id %d successfully removed' %cpu.id

	@rest.restrict('GET')
	def add_nic(self):
		srv_id = int(request.params.get('srv_id'))
		nic_mac = str(request.params.get('nic_mac'))
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
		meta.Session.add(nic)
		meta.Session.commit()
		return 'Nic added successfully id:%d' %nic.mac

	@rest.restrict('GET')
	def del_nic(self):
		print 'API ==> Deleting Nic information'
		nic_mac = str(request.params.get('nic_mac'))
		nic = meta.Session.query(Nic).filter(Nic.mac == nic_mac).one()
		if not nic:
			return 'No such Nic'
		meta.Session.delete(nic)
		meta.Session.commit()
		return 'Nic with macid %s successfully removed' %nic.mac

	@rest.restrict('GET')
	def add_disk(self):
		srv_id = int(request.params.get('srv_id'))
		hdd_size = request.params.get('hdd_size')
		if hdd_size:
			hdd_size = int(hdd_size)
		else:
			hdd_size = 0
		hdd_device = str(request.params.get('hdd_device'))
		hdd = Hdd(srv_id, hdd_device, hdd_size)
		meta.Session.add(hdd)
		meta.Session.commit()
		return 'Disk added successfully device:%s' %hdd.device
	
	@rest.restrict('GET')
	def del_disk(self):
		print 'API ==> Deleting Disk information'
		hdd_device = request.params.get('hdd_device')
		hdd = meta.Session.query(Hdd).filter(Hdd.device == hdd_device).one()
		if not hdd:
			return 'No such Disk'
		meta.Session.delete(hdd)
		meta.Session.commit()
		return 'Disk %s successfully removed' %hdd.device
