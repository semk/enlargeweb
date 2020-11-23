import logging, datetime
import webhelpers.paginate

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from enlargeweb.lib.base import BaseController, render
from enlargeweb.model import meta
from enlargeweb.model.srv import Server
from enlargeweb.model.act import Activity
from sqlalchemy.sql.expression import desc as desc
from routes import url_for
log = logging.getLogger(__name__)

class ActivityController(BaseController):
	requires_auth = True
	
	def list(self):
	    c.list_origin = 'list'
	    return self.build_list(False)

	def running(self):
		c.list_origin = 'running'
		return self.build_list(True)

	def build_list(self, running):
		if not 'page' in request.params:
			page = 1
		else:
			page = request.params['page']
		
		selection = meta.Session.query(Activity).order_by(desc(Activity.start_time))
		if running:
			selection = selection.filter(Activity.status == 1)
			
		c.activities = webhelpers.paginate.Page(
				selection,
                page = int(page),
                items_per_page = 15)
		if 'partial' in request.params:
			return render('activity_list_ajax.mako')
		else:
			# Render the full page
			return render('activity_list.mako')

	def info(self, id):
		c.activity = meta.Session.query(Activity).filter(Activity.id==id).one()
		return render('activity_info.mako')

	def finish(self, id):
		return self.stop('finish', id)

	def cancel(self, id):
		return self.stop('cancel', id)

	def stop(self, action, id):
		message = request.params.get('message')
		activity = meta.Session.query(Activity).filter(Activity.id==id).one()
		c.activity = activity
		c.action = action
		if not action or not message:
		    return render('activity_stop.mako')
		else:
			log.debug('going to %s activity with id=%s' % (action, id))
			#set new activity status according to action
			if action == 'cancel':
				activity.cancel(message, self.get_user_name(), 127)
			else:
				activity.finish(message, self.get_user_name(), 0)
			
			return redirect_to(url_for(action='info', id = activity.id))
