"""Setup the EnlargeWeb application"""
import logging
import md5
from enlargeweb.config.environment import load_environment
from enlargeweb.model import meta

from enlargeweb.model.srv import *
from enlargeweb.model.act import *
from enlargeweb.model.device import *
from enlargeweb.model.dlzbind import *
from enlargeweb.model.act import *
from enlargeweb.model.appl import *
from enlargeweb.model.prop import *
from enlargeweb.model.srv_act import *
from enlargeweb.model.device import *
from enlargeweb.model.user import *

log = logging.getLogger(__name__)

def setup_app(command, conf, vars):
    """Place any commands to setup enlargeweb here"""
    load_environment(conf.global_conf, conf.local_conf)
    # Create the tables if they don't already exist
    log.info('Creating tables')
    meta.metadata.create_all(bind=meta.engine)
    q = meta.Session.query(User).filter(User.login == 'admin')
    if q.count() < 1:
    	log.info('Creating "admin" user.')
    	admin = User(None,
					'admin',
					'Administrator',
					'',
					'System')
    	password = raw_input('Please enter admin password:')
    	admin.password = md5.md5(password).hexdigest()
    	attr = UserAttribute(name = 'rights',
							value = 'admin')
    	admin.attributes.append(attr)
    	meta.Session.add(admin)
    	meta.Session.add(attr)
    	meta.Session.commit()