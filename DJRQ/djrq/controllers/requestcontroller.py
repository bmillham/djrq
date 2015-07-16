import djrq.middleware
import web
from djrq.model import get_current_requests, get_new_pending_requests_info
from basecontroller import BaseController

class RequestController(BaseController):
    def index(self, *args, **kw):
        #kwargs['requests_count'], kwargs['requests_length'] = get_new_pending_requests_info()
        #kwargs['selected_catalogs'] = [1,4]
        return 'djrq.templates.request_list', dict(request_list=get_current_requests(),
                                                   listeners=kw['listeners'],
                                                   requests_length=kw['requests_length'],
                                                   requests_count=kw['requests_count'],
                                                  )