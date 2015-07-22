from web.core import request
import djrq.middleware
import web
from web.core.templating import render
from datetime import datetime
from djrq.model import *
from sqlalchemy.sql import func, or_
from time import time
from ..basecontroller import BaseController
from suggestionscontroller import SuggestionsController
from mistagscontroller import MistagsController
from requestscontroller import RequestsController

class Admin(BaseController):
    suggestions = SuggestionsController()
    mistags = MistagsController()
    requests = index = RequestsController()