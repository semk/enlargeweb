#!/usr/bin/env python
# EnlargeWeb source code
# Licenced under GPLv3
# Stanislav Yudin
import logging, sys, os, threading

from paste.deploy import appconfig
from pylons import config

from service import DhcpServiceImplementation
from enlargeweb.lib.config import Configuration
from enlargeweb.config.environment import load_environment

console_log_level = logging.DEBUG
file_log_level = logging.DEBUG

def setupLog(logPath):
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)

	ch = logging.StreamHandler()
	ch.setLevel(console_log_level)

	fh = logging.FileHandler(logPath)
	fh.setLevel(file_log_level)
	
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

	ch.setFormatter(formatter)
	fh.setFormatter(formatter)

	logger.addHandler(ch)
	logger.addHandler(fh)
	
def dhcpSeviceThread(config, sectionName):
	log = logging.getLogger('dhcpSeviceThread')
	log.info('starting thread for %s' % sectionName)
	server = DhcpServiceImplementation(config, sectionName)
	while True :
		server.GetNextDhcpPacket()
	
if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.stderr.write('Incorrect usage, specify configuration file for service as the only argument\n')
		sys.stderr.write('\tSample: %s path/to/config.ini\n' % sys.argv[0])
		sys.exit(1)
	
	sys.stdout.write('Using configuration file at %s\n' % sys.argv[1])
	if not os.path.exists(sys.argv[1]):
		sys.stderr.write('%s doesn\'t exist. Specify a valid path.\n' % sys.argv[1])
		sys.exit(1)
		
	config = Configuration(sys.argv[1])
	setupLog(config.dhcp.logPath)
	
	log = logging.getLogger('dhcp starter')
	
	# Setup the SQLAlchemy database engine
	conf_path = os.getenv('enlargeweb_config')
	if not conf_path:
		conf_path = os.path.abspath('../development.ini')
	conf = appconfig('config:' + conf_path)
	load_environment(conf.global_conf, conf.local_conf)
	
	#read sections
	sections = []
	rangeNums = config.dhcp.enabledRanges.split(',')
	for rangeNum in rangeNums:
		s = 'range%s' % rangeNum.strip()
		log.info('reading section %s' % s)
		sections.append(s)
	
	#create pidfile before starting threads
	pid = os.getpid()
	pidfile = open('pidfile', 'w')
	pidfile.write(str(pid))
	pidfile.flush()
	pidfile.close()
	
	threads = []
	for s in sections:
		log.info('starting thread for %s' % s)
		th = threading.Thread(target=dhcpSeviceThread, args = (config, s))
		th.start()
		threads.append(th)
		
	log.info('%s threads working' % len(threads))
	try:
		#wait for threads
		for t in threads:
			t.join()
	except KeyboardInterupt:
		sys.exit(0)
	
