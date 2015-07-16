from web.core import request
import djrq.middleware
import web
from web.core.templating import render
from datetime import datetime
from djrq.model import *
from sqlalchemy.sql import func, or_
from time import time
from account import AccountMixIn

class Admin(web.core.Controller, AccountMixIn):
    #def __init__(self, id):
    #    print "Starting admin"
    #    super(Resource, self).__init__()

    def index(self, *args, **kwargs):
        return 'djrq.templates.admin.hello', {}

    def suggestions(self, *args, **kwargs):
        return 'djrq.templates.admin.suggestions', {}