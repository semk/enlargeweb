# EnlargeWeb plugin: Linux OS Deployment / Ubuntu or Debian
# Licenced under GPLv3
# Stanislav Yudin

import os, sys, logging, uuid, datetime
from pxeboot import PxeBoot
from enlargeweb.model import meta
from enlargeweb.model.srv import Server
from enlargeweb.lib.plugins import LibPluginInfo

class PluginUbuntu(PxeBoot):
	info = LibPluginInfo( 'foundation',
					   '22b4e183a19c4b07b60ffb487ca3c8ee',
					   'Ubuntu network deployment',
					  [
						('Configuration', 'preseed', 'enum', 'enum_preseed'),
						('Root password', 'root_password', 'text', None),
						('Kernel arguments', 'kernel_args', 'text', None)
					   ],
					   '/images/ubuntu.png'
					   )
	#All folder paths are nested from EnalrgeWeb root folder
	tftp_folder = 'tftpboot'
	preseed_folder = 'enlargeweb/public/files'
	preseed_pattern = '.preseed'
	
	#address where generated preseeds would be created
	#add accessed by d-i
	public_address = '172.16.75.1:8080'

	#first is url to preseed and 
	#second are arbitary kernel arguments
	pxelinux_config_template = """timeout 5
prompt 1
default enlargeweb
label enlargeweb
    kernel linux
    append  initrd=initrd.gz locale=en_US console-setup/layoutcode=us netcfg/wireless_wep= netcfg/choose_interface=eth0 netcfg/get_hostname= DEBCONF_DEBUG=5 url=%s -- %s
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
			
		#modify preseed according to options
		template_path = os.path.join(self.preseed_folder, '%s%s' % ( args['preseed'], self.preseed_pattern ))
		preseed_file = 'preseed_host-%s_act-%s_appl-%s.cfg' % (self.target.id, self.activity.id, self.args['appl_id'] )
		preseed_path = os.path.join(self.preseed_folder, preseed_file)
		self.put_log('Configuration: %s' % template_path)
		template = open(template_path, 'r')
		lines = template.readlines()
		template.close()
		content = ''
		for line in lines:
			line = line.replace('%password%', args['root_password'])
			content = content + line

		#add ssh key setup line
		content = content + self.get_preseed_ssh_line()
		
		#save real preseed
		real = open(preseed_path, 'w')
		real.write(content)
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
					'http://%s/files/%s' % (self.public_address, preseed_file),
			 		kargs))
		pxe_conf.flush()
		pxe_conf.close()
		
		boot_file = '/%s/pxelinux.0' % target_arch
		self.put_log('Setting boot to %s' % boot_file)
		self.set_boot(self.target, boot_file)
		self.finish_pxe_boot(start_time, target_nic)
		
	def get_preseed_ssh_line(self):
		script_file_name = self.generate_postinstall_script()
		return 'd-i preseed/late_command string wget http://%s/files/%s; sh %s' % ( self.public_address, script_file_name, script_file_name)
		
	def generate_postinstall_script(self, key_path = os.path.expanduser('~/.ssh/id_dsa.pub')):
		#read key file
		key_file = open(key_path, 'r')
		key_content = key_file.readline()
		key_file.close()
		#remove endline from before building command
		key_content = key_content.replace('\n', '')
		#create script
		script_file_name = 'key_host-%s_act-%s_appl-%s.sh' % (self.target.id, self.activity.id, self.args['appl_id'] )
		script_path = os.path.join(self.preseed_folder, script_file_name)
		script_file = open(script_path, 'w')
		# actions to perform on post install
		#add public key
		script_file.write('mkdir -p / /target/root/.ssh\n')
		script_file.write('echo "%s" > /target/root/.ssh/authorized_keys\n' % key_content)
		#disable boot for host
		script_file.write('wget http://%s/api/disable_boot/%s -O /target/root/enlargeweb_boot\n' % (self.public_address, self.args['host_id']))
		#save
		script_file.flush()
		script_file.close()
		return script_file_name

	def enum_preseed(self):
		preseeds = []
		files = os.listdir(self.preseed_folder)
		for f in files:
			if self.preseed_pattern in f:
				preseeds.append(f.replace(self.preseed_pattern, ''))
		return preseeds
