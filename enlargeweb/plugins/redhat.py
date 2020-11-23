# EnlargeWeb plugin: Linux OS Deployment / RedHat based
# Licenced under GPLv3
# Stanislav Yudin

import os, sys, logging, uuid, datetime
from pxeboot import PxeBoot
from enlargeweb.model import meta
from enlargeweb.model.srv import Server
from enlargeweb.lib.plugins import LibPluginInfo

class PluginRedHat(PxeBoot):
	info = LibPluginInfo( 'foundation',
					   'f7648392b7424c5c8944010efa8f98b0',
					   'RedHat network deployment',
					  [
						('Configuration', 'kickstart', 'enum', 'enum_kickstart'),
						('Root password', 'root_password', 'text', None),
						('Boot kernel', 'kernel', 'text', 'rhkernel'),
						('Boot initrd', 'initrd', 'text', 'rhinitrd.gz'),
						('Repository', 'method', 'text', 'http://isoredirect.centos.org/centos/5/os/i386/'),
						('Kernel arguments', 'kernel_args', 'text', None)
					   ],
					   '/images/centos.png')
	#All folder paths are nested from EnalrgeWeb root folder
	tftp_folder = 'tftpboot'
	kickstart_folder = 'enlargeweb/public/files'
	kickstart_pattern = '.kickstart'
	
	#address where generated kickstarts would be created
	#add accessed by anaconda
	public_address = '172.16.75.1:8080'
	pxelinux_config_template = """timeout 5
prompt 1
default enlargeweb
label enlargeweb
    kernel %s
    append  initrd=%s ks=%s method=%s netdevice=%s noipv6 -- %s
"""
	
	def operate(self, args, log):
		start_time = datetime.datetime.now()
		# Read path to development.ini from environment and configure pylons
		self.init(log, args)
		self.put_log('%s started on behalf of %s' % ( args['appl_name'], args['owner'] ))
		
		target_arch = self.target.cpus[0].arch
		#check network configured
		target_nic = self.target.get_main_nic()
		if not target_nic:
			self.activity.cancel(args['owner'], 
								'Server %s doesn\'t have the main adapter configured. Deployment can\'t be continued', 
								-1,
								kill_proc = False)
			return
			
		#generate root password, we are going to setup key auth, so no need to remember it
		if not args['root_password']:
			args['root_password'] = str(uuid.uuid4()).replace('-','')
			#remove me!!!
			self.log.debug('root password: %s' % args['root_password'])
			
		#modify kickstart according to options
		template_path = os.path.join(self.kickstart_folder, '%s%s' % ( args['kickstart'], self.kickstart_pattern ))
		kickstart_file = 'kickstart_host-%s_act-%s_appl-%s.cfg' % (self.target.id, self.activity.id, self.args['appl_id'] )
		kickstart_path = os.path.join(self.kickstart_folder, kickstart_file)
		
		#get public key content
		key_path = os.path.expanduser('~/.ssh/id_dsa.pub')
		key_file = open(key_path, 'r')
		key_content = key_file.readline()
		key_file.close()
		
		self.put_log('Configuration: %s' % template_path)
		template = open(template_path, 'r')
		lines = template.readlines()
		template.close()
		content = ''
		for line in lines:
			line = line.replace('%password%', args['root_password'])
			line = line.replace('%public_key%', key_content)
			content = content + line
		#save real kickstart
		real = open(kickstart_path, 'w')
		real.write(content)
		#call api/disable_boot/hostid in postinstall section
		real.write('wget http://%s/api/disable_boot/%s -O ~root/enlargeweb_boot\n' % (self.public_address, self.args['host_id']))
		real.flush()
		real.close()
		
		#generate config for pxelinux
		if not os.path.exists(self.tftp_folder):
			os.makedirs(self.tftp_folder)
		pxe_conf_folder = os.path.join(self.tftp_folder, target_arch, 'pxelinux.cfg')
		if not os.path.exists(pxe_conf_folder):
			os.makedirs(pxe_conf_folder)
			
		pxe_conf_path = os.path.join(pxe_conf_folder, '01-%s' % target_nic.mac.replace(':', '-' ))
		self.put_log('Creating PXE configuration at %s' % pxe_conf_path)
		pxe_conf = open(pxe_conf_path, 'w')
		kargs = args['kernel_args']
		if not kargs:
			kargs = ''
		pxe_conf.write( self.pxelinux_config_template % (
					self.args['kernel'],
					self.args['initrd'],
					'http://%s/files/%s' % (self.public_address, kickstart_file),
					self.args['method'],
					target_nic.mac,
			 		kargs))
		pxe_conf.flush()
		pxe_conf.close()
		
		boot_file = '/%s/pxelinux.0' % target_arch
		self.put_log('Setting boot to %s' % boot_file)
		self.set_boot(self.target, boot_file)
		self.finish_pxe_boot(start_time, target_nic)

	def enum_kickstart(self):
		kickstarts = []
		files = os.listdir(self.kickstart_folder)
		for f in files:
			if self.kickstart_pattern in f:
				kickstarts.append(f.replace(self.kickstart_pattern, ''))
		return kickstarts
