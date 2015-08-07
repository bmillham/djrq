import djrq.middleware
import web
from djrq.model import *
from web.auth import authorize

class RequestForm(web.core.HTTPMethod):
    def __before__(self, *args, **kw):
        options = session.query(SiteOptions).one()
        kw['options'] = options
        kw['limit_requests'] = options.limit_requests
        return super(RequestForm, self).__before__(*args, **kw)

    def __after__(self, result, *args, **kw):
        kw.update(result)
        return super(RequestForm, self).__after__(('djrq.templates.admin.options.forms.request', kw))

    @authorize(web.auth.authenticated)
    def get(self, *args, **kw):
        return dict(status=None)

    @authorize(web.auth.authenticated)
    def post(self, *args, **kw):
        result = dict(status=None)
        if 'requestlimitfield' in kw:
            limit = int(kw['requestlimitfield'])
            if kw['options'].limit_requests != limit:
                kw['options'].limit_requests = limit
                result['limit_requests'] = limit
                result['status'] = '[Updated]'
                session.commit()
        return result