#!/usr/bin/python

import os, sys, shutil
from enlargeweb.lib.cmnd import run_command

control_template = """
Package: EnlargeWeb
Version: %s-%s
Architecture: all
Depends:
Maintainer: Stanislav Yudin (decvar@gmail.com)
Description: Easy to use open source private and public cloud builder and manager
"""

install_dir = 'opt/enlargeweb'
source_dir = os.path.abspath(os.path.curdir)
target_dir = os.path.join(source_dir, 'deb', 'DEBIAN')

def get_version():
	rc, out = run_command([ '/usr/bin/svnversion', source_dir ])
	if rc != 0:
		print 'failed to get svn version'
		return rc
	version = out.strip()
	return version

def build_control(user_version):
	print 'Bulding control file...'
	print 'Version from %s' % source_dir
	version = get_version()
	print 'Version: %s' % version
	
	control_path = os.path.abspath(os.path.join(target_dir, 'control'))
	print 'Building control file:', control_path
	control = open( control_path, 'w')
	control.write( control_template % (user_version, version) )
	control.flush()
	control.close()
	
	conffiles_path = os.path.abspath(os.path.join(target_dir, 'conffiles'))
	print 'Building conffiles:', conffiles_path
	conffiles = open(conffiles_path, 'w')
	#conffiles.write('development.ini\n')
	#conffiles.write('production.ini\n')
	#conffiles.write('test.ini\n')
	conffiles.flush()
	conffiles.close()

def build_distro():
	distro = {}
	for dirpath, dirnames, filenames in os.walk(source_dir):
		if 'workers' in dirpath:
			continue
		if '.svn' in dirpath:
			continue
		if 'data' in dirpath:
			continue
		if '.cache' in dirpath:
			continue
		if '~' in dirpath:
			continue
		if 'DEBIAN' in dirpath:
			continue
		for f in filenames:
			if '~' in f:
				continue
			if 'pyc' in f:
				continue
			if '.cfg' in f:
				continue
			if '.preseed' in f:
				continue
			if '.kickstart' in f:
				continue
			if '.sh' in f:
				continue
			if '.tmp' in f:
				continue
			source_copy = os.path.join(dirpath, f)
			internal_path = os.path.relpath(source_copy, source_dir)
			target_copy = os.path.join(target_dir, install_dir, internal_path)
			distro[source_copy] = target_copy
			print '%s -> %s' % (source_copy, target_copy)
	return distro

def copy_distro(distro):
	print 'Coping files...'
	one_file = 100 / float(len(distro))
	progress = 0
	for source in distro:
		target = distro[source]
		try:
			os.makedirs(os.path.dirname(target))
		except OSError:
			pass
		shutil.copyfile(source, target)
		progress += one_file
		sys.stdout.write('\r%s' % int(progress))
	print '\nDone!'
		
def build_deb(user_version):
	print 'Building DEB from %s' % os.path.dirname(target_dir)
	rc, out = run_command(['dpkg', '-b', os.path.dirname(target_dir), 'enlargeweb_%s-%s.deb' % (user_version, get_version())])
	if rc != 0:
		print 'failed to build deb:', out
	
def main():
	print 'Source dir:', source_dir	
	print 'Target dir:', target_dir
	rc, out = run_command(['rm', '-fr', target_dir] )
	if rc != 0:
		print 'failed to remove target dir:', out
	os.makedirs(target_dir)
	user_version = "0.1"
	if len(sys.argv) == 2:
		user_version = sys.argv[1]
	build_control(user_version)
	distro = build_distro()
	print '%s files to copy' % len(distro)
	copy_distro(distro)
	build_deb(user_version)
	return 0
	
if __name__ == '__main__':
	print '%s' % sys.argv[0]
	sys.exit(main())
