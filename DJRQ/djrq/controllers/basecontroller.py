import djrq.middleware
import web
from djrq.model import *

class BaseController(web.core.Controller):
    def __before__(self, *args, **kw):
        options = session.query(SiteOptions).one()
        kw['selected_catalogs'] = options.catalog.split(",")
        kw['requests_count'], kw['requests_length'] = get_new_pending_requests_info()
        kw['listeners'] = session.query(Listeners).first()
        if 'nick' not in web.core.session:
            web.core.session['nick'] = ""
        return super(BaseController, self).__before__(*args, **kw)
