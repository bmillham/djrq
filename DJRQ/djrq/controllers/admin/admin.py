from web.core import request
import djrq.middleware
import web
from web.core.templating import render
from datetime import datetime
from djrq.model import *
from sqlalchemy.sql import func, or_
from time import time

from suggestionscontroller import SuggestionsController
from mistagscontroller import MistagsController

class Admin(web.core.Controller):
    #def __init__(self, id):
    #    print "Starting admin"
    #    super(Resource, self).__init__()
    suggestions = SuggestionsController()
    mistags = MistagsController()

    def index(self, *args, **kwargs):
        return 'djrq.templates.admin.hello', {}

    #def suggestions(self, *args, **kwargs):
    #    return 'djrq.templates.admin.suggestions', {}