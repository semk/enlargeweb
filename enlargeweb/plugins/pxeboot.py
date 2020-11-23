import logging, datetime, time
from enlargeweb.model import meta
from enlargeweb.model.srv import BootEntry
from enlargeweb.model.srv import Server
from basic import BasicPlugin
from enlargeweb.lib.ssh import SimpleClient

class PxeBoot(BasicPlugin):
	"""
	Class offers methods to setup a pxe
	boot of specified host into specified boot image
	"""
	
	def set_boot(self, host, boot_file):
		self.log.info('set_boot: host id:%s boot_file:%s' % (host.id, boot_file))
		n = host.get_main_nic()
		#add boot
		self.set_boot_for_hw(n.mac, boot_file)
	
	def set_boot_for_hw(self, hw_addr, boot_file):
		self.log.debug('set_boot_for_hw: hw_addr:%s boot_file:%s' % (hw_addr, boot_file))
		
		be_query = meta.Session.query(BootEntry).filter(BootEntry.mac == hw_addr)
		known_be = be_query.count()
		if known_be > 1:
			self.error('There are more than one boot entry for host (%s). DB is inconsistent.' % known_be, 1)
		elif known_be == 0:
			be = BootEntry(hw_addr, boot_file)
		else:
			be = be_query.one()
			be.file = boot_file
		meta.Session.add(be)
		meta.Session.commit()
	
	def finish_pxe_boot(self, start_time, target_nic):
		"""
		Reboots target host, waits untill it is online
		and checks that /root/enlargeweb_boot is available on target
		"""
		
		#try to reboot target
		self.put_log('Rebooting %s' % target_nic.ip_address)
		if not self.target.reboot(self.log):
			self.put_log('Failed to reboot %s. Manual reboot required.' % target_nic.ip_address)
			
		#make sure that target is offline after attempting to reboot it
		if self.target.online:
			self.activity.error(self.args['owner'], 
								'Target host appears to be online after reboot attempt', 
								-1,
								False)
			return
			
		#wait till host becomes online
		self.put_log('Waiting for host to appear online')
		while True:
			meta.Session.refresh(self.target)
			self.log.info('%s, online: %s' % (str(self.target), self.target.online) )
			if self.target.online:
				break			
			time.sleep(15)
		self.put_log('Host reported online, trying to access')
		
		#try to access host via ssh
		ssh = self.target.get_ssh(self.log)
		while True:
			ret = ssh.execute('cat /root/enlargeweb_boot')
			self.log.info('ssh ret code:%s' % ret)
			if ret == 0:
				break
			time.sleep(60)
			
		self.activity.finish(self.args['owner'], 
							'Deployment complete in %s secs' % ( (datetime.datetime.now() - start_time).seconds),
							0,
							False)
