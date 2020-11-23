#!/usr/bin/env python
# EnlargeWeb source code
# Licenced under GPLv3
# Stanislav Yudin

import logging, sys, os, signal

if __name__ == '__main__':
	pidfile = 'pidfile'
	if len(sys.argv) >= 2:
		pidfile = sys.argv[1]
	file = open(pidfile, 'r')
	pid = int(file.readline())
	print 'Stopping service: %s' % pid	
	os.kill(pid, signal.SIGKILL)
    
    
