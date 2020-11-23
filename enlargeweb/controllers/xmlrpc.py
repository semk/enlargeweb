import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from enlargeweb.lib.base import BaseController, render

log = logging.getLogger(__name__)

class XmlrpcController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/xmlrpc.mako')
        # or, return a response
        return 'Hello World'
