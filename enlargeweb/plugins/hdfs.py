# EnlargeWeb plugin: Hadoop File System Node plugin
# Licenced under GPLv3
# Stanislav Yudin

import os, sys, datetime
from enlargeweb.lib.plugins import LibPluginInfo
from basic import BasicPlugin

class PluginHDFS(BasicPlugin):
	info = LibPluginInfo( 'application',
					   '988c2d64d18a4248a0a8beaf8a80cee7',
					   'HDFS Node',
					  [
					  	('Java home', 'java', 'text', '/usr/lib/jvm/java-6-sun'),
					  	('Package url', 'url', 'text', 'http://mirrors.ibiblio.org/pub/mirrors/apache/hadoop/core/hadoop-0.20.1/hadoop-0.20.1.tar.gz'),
						('Configuration', 'mode', 'enum', 'enum_modes'),
					   ],
					   )
					   
	work_folder = '~root/hdfs_installer/'
	
	#config for Pseudo-Distributed Mode
	pseudo_conf_core_site = """<configuration>
	<property>
		<name>fs.default.name</name>
		<value>hdfs://localhost:9000</value>
	</property>
</configuration>"""
	pseudo_conf_hdfs_site = """<configuration>
  <property>
    <name>dfs.replication</name>
    <value>1</value>
  </property>
</configuration>"""
	pseude_conf_mapred_site = """<configuration>
  <property>
    <name>mapred.job.tracker</name>
    <value>localhost:9001</value>
  </property>
</configuration>"""
	
	def get_filename(self, url):
		parts = url.split('/')
		return parts[len(parts)-1]
		
	def get_inner_folder(self, file_name):
		return file_name.rsplit('.', 2)[0]#file_name[file_name.find('-')+1 : file_name.find('tar')-1]
	
	def operate(self, args, log):
		self.init(log, args)
		start_time = datetime.datetime.now()
		
		#download tarball to target
		ssh = self.target.get_ssh()
		ssh.execute_command(['mkdir', '-p', self.work_folder])
		self.put_log('Downloading Hadoop from %s' % self.args['url'] )
		rc, out = ssh.execute_command(['wget', '-P', self.work_folder, self.args['url']])
		if rc!= 0:
			self.activity.error(self.args['owner'], 'Failed to download installer', -1, False)
			return
		
		downloaded_path = os.path.join(self.work_folder, self.get_filename(self.args['url']))
			
		#unpack tarball
		ssh.execute_command(['mkdir', '-p', '/opt/hadoop'])
		self.put_log('Unpacking the %s to /opt/hadoop' %downloaded_path)
		rc, out = ssh.execute_command(['tar', 'xzf', downloaded_path, '-C', '/opt/hadoop'])
		if rc != 0:
			self.activity.error(self.args['owner'], 'Failed to unpack %s' % downloaded_path, -1, False)
			return
			
		unpacked_folder = os.path.join('/opt/hadoop', self.get_inner_folder(self.get_filename(self.args['url'])))
		
		#setting java home
		java_env = 'JAVA_HOME=%s' %self.args['java']
		if ssh.execute_command(['echo', java_env, '>>', os.path.join(unpacked_folder, 'conf/hadoop-env.sh')]) [0] != 0:
			self.activity.error(self.args['owner'], 'Error setting JAVA_HOME', -1, False)
			return
		
		#handle modes
		if self.args['mode'] == 'Local (Standalone) Mode':
			#local is by default
			self.put_log('Local (Standalone) Mode - Configuration applied')
		elif self.args['mode'] == 'Pseudo-Distributed Mode':
			ssh.execute_command('echo "%s" >> %s', self.pseudo_conf_core_site, os.path.join(unpacked_folder, 'conf/core-site.xml'))
			ssh.execute_command('echo "%s" >> %s', self.pseudo_conf_hdfs_site, os.path.join(unpacked_folder, 'conf/hdfs-site.xml'))
			ssh.execute_command('echo "%s" >> %s', self.pseude_conf_mapred_site, os.path.join(unpacked_folder, 'conf/mapred-site.xml'))
			self.put_log('Pseudo-Distributed Mode - Configuration applied')
		else:
			self.put_log('Fully-Distributed Mode - Not supported')
		
		#call start-all
		self.put_log('Execuing Start-All')
		rc, out = ssh.execute_command(['cd', unpacked_folder, '&&', 'bin/start-all.sh'])
		if rc != 0:
			self.put_log(out)
			self.activity.error(self.args['owner'], 'Start-All failed with code = %s' % rc, int(rc), False)
			return
		#done
		self.activity.finish(self.args['owner'], 
							'Deployment complete in %s secs' % ( (datetime.datetime.now() - start_time).seconds),
							0,
							False)
		
	def enum_modes(self):
		return [	
					'Local (Standalone) Mode',
					'Pseudo-Distributed Mode',
					'Fully-Distributed Mode'
				]
