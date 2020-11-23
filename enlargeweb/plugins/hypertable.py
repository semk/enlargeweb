"""
EnlargeWeb: plugin for HyperTable Deployment

Written By: Sreejith K
"""

import os, sys, datetime
from enlargeweb.lib.plugins import LibPluginInfo
from basic import BasicPlugin

class PluginHypertable(BasicPlugin):
    info = LibPluginInfo('application',
            'f8f1e1e1fbed4d598fe8f63abdb30a3f',
            'Hypertable Deployment',
            [
                ('Package Url', 'url', 'text', 'http://package.hypertable.org/hypertable-0.9.2.7-linux-i386.tar.bz2'),
                ('Mode', 'mode', 'enum', 'enum_modes'),
                ('HDFS Directory', 'hdfs_dir', 'text', '/opt/hadoop/hadoop-0.20.1/'),
                ],
            )
    
    work_folder = '~root/hypertable_installer/'

    def get_filename(self, url):
        parts = url.split('/')
        return parts[len(parts)-1]

    def get_inner_folder(self, filename):
        return filename.rsplit('.', 2)[0]

    def get_version(self, path):
        inner = self.get_inner_folder(path)
        return inner.rsplit('-', 3)[1]

    def operate(self, args, log):
        self.init(log, args)
        start_time = datetime.datetime.now()

        # Download Hypertable
        ssh = self.target.get_ssh()
        ssh.execute_command(['mkdir', '-p', self.work_folder])
        self.put_log('Downloading Hypertable from %s' % self.args['url'] )
        if ssh.execute_command(['wget', '-P', self.work_folder, self.args['url']] ) [0] != 0:
            self.activity.error(self.args['owner'], 'Failed to download installer', -1, False)
            return

        downloaded_path = os.path.join(self.work_folder, self.get_filename(self.args['url']))

        # Unpack the package
        self.put_log('Unpacking %s' %downloaded_path)
        if ssh.execute_command(['tar', 'xjf', downloaded_path, '-C', self.work_folder]) [0] !=0:
            self.activity.error(self.args['owner'], 'Failed to unpack %s' % downloaded_path, -1, False)
            return

        unpacked_folder = os.path.join(self.work_folder, self.get_inner_folder(self.get_filename(self.args['url'])))
        content_folder = os.path.join(unpacked_folder, 'opt/hypertable')
        hyp_version = self.get_version(self.args['url'])
        content_folder = os.path.join(content_folder, hyp_version)
        
        install_dir = os.path.join('/opt/hypertable', hyp_version)
        ht_lib_dir = os.path.join(install_dir, 'lib')
        ht_bin_dir = os.path.join(install_dir, 'bin')
        ht_conf_dir = os.path.join(install_dir, 'conf')

        # Copy the contents to /opt/hypertable
        self.put_log('Installing Hypertable')
        ssh.execute_command(['mkdir', '-p', '/opt/hypertable'])
        if ssh.execute_command(['mv', content_folder, '/opt/hypertable']) [0] != 0:
            self.activity.error(self.args['owner'], 'Failed to install Hypertable', -1, False)
            return

        # Configure dynamic linker run-time bindings for hypertable
        #if ssh.execute_command(['echo', ht_lib_dir, '>', '/etc/ld.so.conf.d/hypertable.conf']) != 0:
        #    self.activity.error(self.args['owner'], 'Failed to configure linker for hypertable', -1, False)
        #    return
        
        #if ssh.execute_command(['/sbin/ldconfig']) != 0:
        #    self.activity.error(self.args['owner'], 'ldconfig failed', -1, False)
        #    return

        # Setting up HyperTable environment variables
        if ssh.execute_command(['export', 'LD_LIBRARY_PATH=%s' % ht_lib_dir]) [0] != 0:
            self.activity.error(self.args['owner'], 'Failed to set LD_LIBRARY_PATH', -1, False)
            return

        # Setting up hypertable config files

        # Start hypertable
        if self.args['mode'] == 'Local':
            self.put_log('Starting hypertable locally..')
            rc, out = ssh.execute_command(['cd', install_dir, '&&', 'bin/start-all-servers.sh', 'local'])
        elif self.args['mode'] == 'HDFS':
            # Create directories for hypertable on hdfs and set the permissions.
            self.put_log('Setting up Hypertable directory /hypertable on HDFS')
            rc, out = ssh.execute_command(['cd', self.args['hdfs_dir'], '&&', 
                                            'bin/hadoop', 'fs', '-mkdir', '/hypertable', '&&', 
                                            'bin/hadoop', 'fs', '-chmod', '777', '/hypertable'])
            if rc != 0:
                self.put_log(out)
                self.activity.error(self.args['owner'], 'Creating hypertable directories in HDFS failed with code = %s' % rc, int(rc), False)
                return
            
            # Now it is safe to start Hypertable
            self.put_log('Starting hypertable over HDFS..')
            rc, out = ssh.execute_command(['cd', install_dir, '&&', 'bin/start-all-servers.sh', 'hadoop'])
        
        if rc != 0:
            self.put_log(out)
            self.activity.error(self.args['owner'], 'Start-All-Servers failed with code = %s' % rc, int(rc), False)
            return

        # Hurray !!! Hypertable is deployed successfully.
        self.activity.finish(self.args['owner'], 
                'Deployment completed in %s secs' % ( (datetime.datetime.now() - start_time).seconds),
                0,
                False)

    def enum_modes(self):
        return ['Local',
                'HDFS'
                ]

