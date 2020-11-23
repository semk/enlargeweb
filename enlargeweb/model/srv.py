"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm
from enlargeweb.model import meta
from enlargeweb.model.meta import Base
from sqlalchemy.types import *
from enlargeweb.model.act import Activity
from enlargeweb.model.srv_act import ServerActivity, srvact_collection
from enlargeweb.model.prop import Property
from enlargeweb.model.device import Device
from enlargeweb.model.appl import Appliance
from sqlalchemy import select
import sys, logging, datetime
from enlargeweb.lib.ssh import SimpleClient

log = logging.getLogger(__name__)

node_device_table = sa.Table(
	'node_device', meta.metadata,
	sa.Column('node_id', sa.ForeignKey('node.id')),
	sa.Column('device_id', sa.ForeignKey('device.id'))
)

class BootEntry(Base):
	"""
	class represents boot configuration entry for pxe/dhcp service
	"""
	__tablename__ = 'boot'

	mac = sa.Column(String(17), primary_key = True)
	file = sa.Column( Unicode(64) )

	def __init__(self, mac, boot_file):
		self.mac = mac
		self.file = boot_file

class Nic(Base):
	"""class represents network interface of host"""

	__tablename__ = 'nic'

	node_id = sa.Column( Integer, sa.ForeignKey('node.id'), nullable = False)
	mac = sa.Column(String(17), primary_key = True)
	ip_address = sa.Column(String(15), nullable = False)
	ip_mask = sa.Column(String(15), nullable = False)
	main = sa.Column(Boolean, nullable = False)
	ssh_port = sa.Column(Integer, nullable = False, default = 22)

	def __init__(self, node_id, mac, ip_address, ip_mask, main, ssh_port):
		self.node_id = node_id
		self.mac = mac
		self.ip_address = ip_address
		self.ip_mask = ip_mask
		self.main = main
		self.ssh_port = ssh_port

	def __repr__(self):
		return "%s/%s [%s] port:%s basic:%s" % (self.ip_address, self.ip_mask, self.mac, self.ssh_port, self.main)

sa.Index('ix_nic_ip_addr', Nic.__table__.c.ip_address)

class Hdd(Base):
	"""Class represents HDD device information"""

	__tablename__ = 'hdd'

	node_id = sa.Column( Integer, sa.ForeignKey('node.id'), primary_key = True )
	device = sa.Column( Unicode(64), primary_key = True )
	size = sa.Column( Integer, primary_key = True )

	def __init__(self, node_id, device, size):
		self.node_id = node_id
		self.device = device
		self.size = size

	def __repr__(self):
		return "<Hdd(node:%d, name:%s, size:%s)>" % \
				(self.node_id, self.device, self.size)

class Cpu(Base):
	"""Class represents CPU information"""

	__tablename__ = 'cpu'

	node_id = sa.Column(Integer, sa.ForeignKey('node.id'), nullable = False)
	id = sa.Column( Integer, primary_key = True )
	arch = sa.Column( String(6) )
	speed = sa.Column( SmallInteger )
	model = sa.Column( Unicode(64) )

	def __init__(self, id, arch, speed, model):
		self.id = id
		self.arch = arch
		self.speed = speed
		self.model = model

	def __repr__(self):
		return "<Cpu(id: %d, arch:%s, model:%s)>" % \
				(self.id, self.arch, self.model)


class Memory(Base):
	"""Class represents memory information"""

	__tablename__ = 'memory'

	node_id = sa.Column( Integer, sa.ForeignKey('node.id'), primary_key = True )
	type = sa.Column( Unicode(64), primary_key = True )
	size = sa.Column( Integer, primary_key = True)
	speed = sa.Column( Integer, primary_key = True)

	def __init__(self, node_id, type, size, speed):
		self.node_id = node_id
		self.type = type
		self.size = size
		self.speed = speed

	def __repr__(self):
		return "<Memory(node:%d, type:%s, size:%d, speed:%d)>" % \
				(self.id, self.type, self.size, self.self.speed)


class ServerAppliance(Base):
	"""
	Class represents deployed appliance
	"""

	__tablename__ = 'node_appliance'

	node_id = sa.Column(Integer, sa.ForeignKey('node.id'), primary_key = True)
	appliance_id = sa.Column(Integer, sa.ForeignKey('appliance.id'), primary_key = True)
	activity_id = sa.Column(Integer, sa.ForeignKey('activity.id'), primary_key = True)

	appliance_info = orm.relation(Appliance, cascade = 'all')
	activity_info = orm.relation(Activity , cascade = 'all')
	
	def __str__(self):
		return 'node_id:%s appl_id:%s activity_id:%s' % ( self.node_id, self.appliance_id, self.activity_id )

class Attribute(Base):
	"""
	Class represents internal server attributes
	"""
	__tablename__ = 'node_attributes'

	node_id = sa.Column(Integer, sa.ForeignKey('node.id'), primary_key = True)
	name = sa.Column(String(64))
	value = sa.Column(String(64))

class Server(Base):
	"""class represents hardware node information"""

	__tablename__ = 'node'

	id = sa.Column(Integer, primary_key = True)
	name = sa.Column(Unicode(64))
	department = sa.Column(Unicode(64))
	owner = sa.Column(Unicode(64))
	location = sa.Column(Unicode(64))
	comments = sa.Column(UnicodeText)
	online = sa.Column(Boolean)
	type = sa.Column(Integer)

	activities = orm.relation(
		ServerActivity,
		backref = orm.backref('server_info'),
		collection_class = srvact_collection('activity_info'),
		cascade='all'
	)

	nics = orm.relation(Nic, cascade='all')
	cpus = orm.relation(Cpu, cascade='all')
	hdds = orm.relation(Hdd, cascade='all')
	appliances = orm.relation(ServerAppliance, cascade='all')
	devices = orm.relation(Device, secondary = node_device_table, cascade='all')
	attributes = orm.relation(Attribute, cascade='all')

	def __init__(self, id, name, department, owner, location, comments, online, type):
		self.id = id
		self.name = name
		self.department = department
		self.owner = owner
		self.location = location
		self.comments = comments
		self.online = online
		self.type = type
		
	def get_activities(self, reverse = True):
		"""
		Method to get sorted activities of host
		returns tuple of lists, running activites first,
		historic second
		"""
		h = []
		r = []
		for a in self.activities:
			if a.activity_info.end_time:
				h.append(a.activity_info)
			else:
				r.append(a.activity_info)
		
		cmpf = lambda a,b: cmp(a.start_time, b.start_time)
		r.sort(cmpf, reverse = reverse)
		h.sort(cmpf, reverse = reverse)
		return r, h 
		
	def reboot(self, log = None):
		if log:
			log.debug('Server.reboot called')
		ssh = self.get_ssh(log)
		self.online = False
		ret = ssh.execute('shutdown -r now', stdout = sys.stdout)
		if log:
			log.debug('Server.reboot rc=%s' % ret)
		return  ( ret == 0 )
	
	def get_ssh(self, log = None, user = 'root'):
		if log:
			log.debug('Server.get_ssh called')
		conn_string =  user + '@' + str(self.get_main_nic().ip_address)
		client = SimpleClient(conn_string, log = log)
		if log:
			log.debug('Server.get_ssh created a ssh client')
		return client
		
	def get_os(self):
		os = 'Unknown OS'
		for a in self.appliances:				
			if 'ubuntu' in a.appliance_info.name.lower():
				os = 'Ubuntu'
				break
			elif 'centos' in a.appliance_info.name.lower():
				os = 'CentOS'
				break
			elif 'redhat' in a.appliance_info.name.lower():
				os = 'RedHat'
				break
		return os
	
	@classmethod
	def list_departments(cls):
		results = meta.Session.execute(select([Server.department], distinct=True))
		return results

	def get_arch(self):
		if len(self.cpus) == 0:
			return 'Unknown'
		else:
			return self.cpus[0].arch

	def get_type(self):
		if self.type == 0:
			return 'PC'
		else:
			return 'Mac'

	def get_main_nic(self):
		if len(self.nics) == 0:
			return None

		for each in self.nics:
			if each.main:
				return each

		return None

	def get_main_nic_text(self):
		n = self.get_main_nic()
		if n == None:
			return 'Not configured.'
		else:
			return n.ip_address

	def __str__(self):
		if self.id:
			return self.name
		else:
			return 'New Server'



