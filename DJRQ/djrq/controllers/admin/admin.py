from web.core import request
import djrq.middleware
import web
from web.auth import authorize
from web.core.templating import render
from datetime import datetime
from djrq.model import *
from sqlalchemy.sql import func, or_
from time import time
from account import AccountMixIn

web.auth.in_group = web.auth.ValueIn.partial('groups')
web.auth.has_permission = web.auth.ValueIn.partial('permissions')

class Admin(web.core.Controller, AccountMixIn):
    #def __init__(self, id):
    #    print "Starting admin"
    #    super(Resource, self).__init__()

    @authorize(web.auth.authenticated)
    def index(self, *args, **kwargs):
        return 'djrq.templates.admin.hello', {}
    
    @authorize(web.auth.authenticated)
    def suggestions(self, *args, **kwargs):
        return 'djrq.templates.admin.suggestions', {}