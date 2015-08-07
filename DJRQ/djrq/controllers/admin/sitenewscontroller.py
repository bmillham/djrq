import djrq.middleware
import web
from djrq.model import *
from ..basecontroller import BaseController
from web.auth import authorize

class SiteNewsController(BaseController):
    def index(self, *args, **kw):
        return 'djrq.templates.admin.sitenews', kw
