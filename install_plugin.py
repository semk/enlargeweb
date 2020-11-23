#!/usr/bin/python
import os, sys
from pylons import config

def install_controller(path):
    print 'Controllers path:%s' % config['pylons.paths']['controllers']
    print 'Plugin: %s' % os.path.basename(path)
    if not os.path.exits(path):
        print 'File do not exists: %s' % path
        return 1
    rc = os.system('ln -s %s %s' % (
            path,
            os.path.join(config['pylons.paths']['controllers'],
                         os.path.basename(path))
            ))
    if rc != 0:
        print 'Plugin install failed: %s' % rc
        return rc
    print 'Done!'
    return 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: %s path/to/controller.py' % sys.argv[0]
        sys.exit(1)
    sys.exit(install_controller(sys.argv[1]))
