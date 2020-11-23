import logging
import webhelpers.paginate
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from enlargeweb.model import meta
from enlargeweb.model.user import User, UserAttribute
from enlargeweb.lib.base import BaseController, render
from routes import url_for
import hashlib
from sqlalchemy.sql.expression import desc

log = logging.getLogger(__name__)

class AccountController(BaseController):
	def list(self):
		if not 'page' in request.params:
			page = 1
		else:
			page = request.params['page']
		c.users = webhelpers.paginate.Page(
			meta.Session.query(User).order_by(desc(User.login)),
			page = int(page),
			items_per_page = 15)
		
		if 'partial' in request.params:
			return render('user_list_ajax.mako')
		else:
			# Render the full page
			return render('user_list.mako')
	
	def login(self):
		return render('login.mako')

	def auth(self):
		identity = session.get('repoze.who.identity')
		if not identity is None:
			if session.get('came_from'):
				log.debug('redirecting to %s' % session['came_from'])
				return redirect_to(session['came_from'])
			else:
				log.debug('redirecting to /host/list [default]')
				return redirect_to(url_for(controller = 'host', action = 'list'))
		else:
			log.fatal('AUTH: account.auth received no indentity')
			
		
		
	def logout(self):
		identity = session.get('repoze.who.identity')
		if not identity:
			log.info('no identity, redirecting to login page.')
		else:
			log.error('identity %s in LOGOUT!' % identity)
			
		return redirect_to(url_for(action = 'login'))
	
	def add(self):
		# Create a new user account
		c.user = User(None, '', '', '', '')
		return render('user_edit.mako')

	def edit(self, id):
		# Use the existing user account
		c.user = meta.Session.query(User).filter(User.id == id).first()
		if not c.user:
			# Create a new user account
			c.user = User(None, '', '', '', '')
		return render('user_edit.mako')

	def save(self):
		if not self.get_user_info():
			c.user = User(None, '', '', '', '')
			return render('user_edit.mako')

		if c.user_id == '':
			c.user_id = None

		user = User(
				c.user_id,
				c.account_name,
				c.first_name,
				c.second_name,
				c.department)
		
		if user.id:
			# Update the account info
			user = meta.Session.merge(user)
			meta.Session.update(user)
			user = meta.Session.query(User).filter(User.id == user.id).one()
			attr = user.get_attr('rights')
			attr.value = c.rights
			attr = meta.Session.merge(attr)
			meta.Session.update(attr)
		else:
			# Create a new account
			user.password = hashlib.md5(c.account_pwd).hexdigest()
			attr =  UserAttribute(name = 'rights',
					value = c.rights)
			user.attributes.append(attr)
			meta.Session.add(user)
			meta.Session.add(attr)
		meta.Session.commit()

		return redirect_to(url_for(action = 'info', id = user.id))

	def get_user_info(self):
		c.user_id = request.params.get('user_id')
		c.account_name = request.params.get('account_name')
		print 'Account name', c.account_name
		
		if not c.account_name:
			c.error = 'Provide Login name'
			return False

		if not c.user_id:
			c.account_pwd = request.params.get('account_pwd')
			print 'Account Password', c.account_pwd
			if not c.account_pwd:
				c.error = 'Please provide password'
				return False

		c.first_name = request.params.get('first_name')
		c.second_name = request.params.get('second_name')
		c.department = request.params.get('department')
		c.rights = request.params.get('rights')

		print 'Account Details', c.first_name, c.second_name, c.department, c.rights
		return True

	def info(self, id):
		c.user = meta.Session.query(User).filter(User.id == id).one()
		return render('user_info.mako')

	def delete(self, id):
		# Remove the account info
		c.user = meta.Session.query(User).filter(User.id == id).first()
		if c.user:
			meta.Session.delete(c.user)
			meta.Session.commit()
		
		# Remove attributes
		c.user_attr = meta.Session.query(UserAttribute).filter(UserAttribute.user_id == c.user.id).first()
		if c.user_attr:
			meta.Session.delete(c.user_attr)
			meta.Session.commit()
		return redirect_to(url_for(action = 'list', id = None))

	def changepass(self, id):
		c.user = meta.Session.query(User).filter(User.id == id).first()
		if not c.user:
			c.user =  User(None, '', '', '', '')
			c.error = 'User does not exist'

		return render('user_change.mako')

	def applypass(self):
		if not self.get_passwords():
			c.user =  meta.Session.query(User).filter(User.id == c.user_id).first()
			return render('user_change.mako')

		if c.user_id == '':
			c.user_id = None
		
		user = meta.Session.query(User).filter(User.id == c.user_id).first()
		current_md5 = hashlib.md5(c.current_password).hexdigest()
		# Update the password
		if current_md5 == user.password:
			user.password = hashlib.md5(c.new_password).hexdigest()
			user = meta.Session.merge(user)
			meta.Session.update(user)
			meta.Session.commit()
		else:
			c.error = 'Wrong Password Given'
			c.user =  meta.Session.query(User).filter(User.id == c.user_id).first()
			return render('user_change.mako')
		
		return redirect_to(url_for(action = 'info', id = user.id))

	def get_passwords(self):
		c.user_id = request.params.get('user_id')
		if not c.user_id:
			c.error = 'User not existing'
			print '>>>>>>>>>>>>>>>>>>>> account.get_passwords, User does not exist' 
			return False

		c.current_password = request.params.get('current_password')
		print '>>>>>>>>>>>>>>>>>>>> account.get_password, Current password:', c.current_password 
		if not c.current_password:
			c.error = 'Provide the Current Password'
			print '>>>>>>>>>>>>>>>>>>>> account.get_password, Provide Current password' 
			return False
		
		c.new_password = request.params.get('new_password')
		if not c.new_password:
			c.error = 'Provide a new Password'
			print '>>>>>>>>>>>>>>>>>>>> account.get_password, Provide new Password' 
			return False

		return True
